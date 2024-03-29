import os
import numpy as np
import pandas as pd
import time
import csv

from ortools.linear_solver import pywraplp

from fd_gpd._fantasyml import neuterPredictions
from fd_gpd._predict.player_stats.helpers import fanduel_ticket_optimized, salary_arb
from fd_gpd._predict.optimize.optimize_proj import fantasyze_proj

import statistics


#creates a master file with all information needed 
#in order ot properly optimize a selected amount of teams
#i.e. create an upload ticket for a given contest
#using the machine learning models predicted probas.
def prepare(model='ensemble', neuter=False, slate_date='', removals=[]):

  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
  path2 ='C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\optmized_team_pools\\{1}\\'.format(user,slate_date)
  path3 = os.getcwd() + r"\fd_gpd\_predict\player_stats\by_week"

  predictions = pd.read_csv(path+'_predict\\gpd\\ml_predictions\\{0}\\dataiku_download_{1}.csv'.format(slate_date, model))
  predictions.rename(columns={'proba_1.0':'proba_1'}, inplace=True)
  predictions = predictions.sort_values(by='proba_1', ascending=False).iloc[:100000]
  predictions = predictions.sort_values(by='lineup',ascending=False) 
  

  onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
  teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

  ##stats = pd.read_csv(path3 + "\\" + '{0}.csv'.format(slate_date)) 
  stats = salary_arb(slate_date=slate_date)
  stats = stats.set_index('RylandID_master')

  teams = teams[teams['lineup'].isin(predictions['lineup'].unique())]
  teams = teams.set_index('name').join(stats, how='inner', lsuffix='_ot').reset_index()

  
  nine_confirm = teams.groupby('lineup').apply(lambda x: len(x))
  teams = teams.set_index('lineup').loc[nine_confirm[nine_confirm==9].index.tolist()].reset_index()
  

  removedf = pd.DataFrame(teams.groupby('lineup').apply(lambda x: sorted(x['Id'].tolist())))
  removedf['isremove'] = removedf[0].apply(lambda x: len(list(set(x).intersection(set(removals)))))
  keepers = removedf[removedf['isremove']==0].index.unique().tolist()

  teams = teams.set_index('lineup').loc[keepers].reset_index()

  if neuter==True:
      nps = neuterPredictions(1, predictions)[['lineup','proba_1_neutralized']].set_index('lineup')
      predictions = predictions.set_index('lineup').join(nps)
      predictions.reset_index(inplace=True)
      predictions['proba_1'] = predictions['proba_1_neutralized']
      predictions.drop(['proba_1_neutralized'], axis=1, inplace=True)

  picks = predictions[['lineup', 'proba_1']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
  picks['proba_rank'] = picks['proba_1'].rank(method='max', ascending=False)/9
  picks['check4max'] = picks.groupby(level=0)['team_team'].value_counts().max(level=0)
  picks = picks[picks['check4max']<4]
  picks.sort_values(by='proba_1', ascending=False, inplace=True)

  return picks, stats


#customized NHL ticket optimizer 
class Player:
  def __init__(self, opts):
    self.proba1 = round(float(opts['proba_1']),4)
    self.rank = int(float(opts['proba_rank']))
    self.lineup = str(opts['lineup'])
    self.team_proj = round(float(opts['team_proj']),4)
    self.team_pm = round(float(opts['team_+/-']),4)
    self._1 = str(opts['1'])
    self._2 = str(opts['2'])
    self._3 = str(opts['3'])
    self._4 = str(opts['4'])
    self._5 = str(opts['5'])
    self._6 = str(opts['6'])
    self._7 = str(opts['7'])
    self._8 = str(opts['8'])
    self._9 = str(opts['9'])
    self.pred_owns = []
    self.lock = False
    self.ban = False
    

  def __repr__(self):
    return "[{0},{1},{2},{3}]".format(self.proba1,self.rank,self.lineup,self.team_proj)
                                    
class Roster:

  POSITION_ORDER = {
    "TEAM": 1,
  }

  def __init__(self):
    self.players = []

  def add_player(self, player):
    self.players.append(player)
  
  def sum_actual(self):
     return round(sum(map(lambda x: x.proba1, self.players)),2)
  
  def mean_actual(self):
     return round(statistics.mean(map(lambda x: x.proba1, self.players)),4)

  def min_actual(self):
     return min(map(lambda x: x.proba1, self.players))

  def max_actual(self):
     return max(map(lambda x: x.proba1, self.players))
  
  def min_proj(self):
     return min(map(lambda x: x.team_proj, self.players))
  
  def max_proj(self):
     return max(map(lambda x: x.team_proj, self.players))
  
  def mean_proj(self):
     return round(statistics.mean(map(lambda x: x.team_proj, self.players)),2)

  def min_pm(self):
     return min(map(lambda x: x.team_pm, self.players))
  
  def max_pm(self):
     return max(map(lambda x: x.team_pm, self.players))
  
  def mean_pm(self):
     return round(statistics.mean(map(lambda x: x.team_pm, self.players)),2)
    
  

  def __repr__(self):
    s = "Sum Proba1: %s" % self.sum_actual()
    s += "\nMin Proba1: %s" % self.min_actual()
    s += "\nMax Proba1: %s" % self.max_actual()
    s += "\nMean Proba1: %s" % self.mean_actual()
    s += "\nMin Proj: %s" % self.min_proj()
    s += "\nMax Proj: %s" % self.max_proj()
    s += "\nMean Proj: %s" % self.mean_proj()
    s += "\nMin Plus/Minus: %s" % self.min_pm()
    s += "\nMax Plus/Minus: %s" % self.max_pm()
    s += "\nMean Plus/Minus: %s" % self.mean_pm()
    return s

def run(roster_size=150, own_limits='', slate_date=''):

  solver = pywraplp.Solver('FD', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  all_players = []  
  user = os.getlogin()
  path = "C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\ml_predictions\\{1}\\".format(user, slate_date)

  with open(path+ r'optimtkttemp.csv', 'r') as csvfile:
    csvdata = csv.DictReader(csvfile, skipinitialspace=True)
    for row in csvdata:
      all_players.append(Player(row)) #this is adding a TEAM, each row is a TEAM at this level

  variables = []
  all_players = np.random.choice(all_players, size=int(len(all_players))
      , replace=False)
  for player in all_players:
    if player.lock:
      variables.append(solver.IntVar(1, 1, player.lineup))
    elif player.ban:
      variables.append(solver.IntVar(0, 0, player.lineup))
    else:      
      variables.append(solver.IntVar(0, 1, player.lineup))
    
  objective = solver.Objective()
  objective.SetMaximization()
  
  for i, player in enumerate(all_players):
    objective.SetCoefficient(variables[i], player.proba1)
     
  size_cap = solver.Constraint(roster_size, roster_size)
  for variable in variables:
    size_cap.SetCoefficient(variable, 1)

  for position, min_limit, max_limit in own_limits:
    position_cap = solver.Constraint(min_limit, max_limit)

    #variables[i] (i is integer) returns lineup_46259_28
    for i, player in enumerate(all_players):
      #position = 
      if position == player._1:
        position_cap.SetCoefficient(variables[i], 1)
      if position == player._2:
        position_cap.SetCoefficient(variables[i], 1)
      if position == player._3:
        position_cap.SetCoefficient(variables[i], 1)
      if position == player._4:
        position_cap.SetCoefficient(variables[i], 1)
      if position == player._5:
        position_cap.SetCoefficient(variables[i], 1)
      if position == player._6:
        position_cap.SetCoefficient(variables[i], 1)
      if position == player._7:
        position_cap.SetCoefficient(variables[i], 1)
      if position == player._8:
        position_cap.SetCoefficient(variables[i], 1)
      if position == player._9:
        position_cap.SetCoefficient(variables[i], 1)

  solution = solver.Solve()

  if solution == solver.OPTIMAL:
    roster = Roster()

    for i, player in enumerate(all_players):
      if variables[i].solution_value() == 1:
        roster.add_player(player)

  else:
    print("No solution :(")
    
  return roster

def slate_optimization(slate_date='1.18.23', model='ensemble', roster_size=150, removals=[], pct_from_opt_proj=.82, max_pct_own=.34, dksalary_min=50000, optimization_pool=int(100000), neuter=False):

  start_time = time.time()
  print('initiating dfs calculations''')

  #prepare ticket optimization file
  prepared = prepare(neuter=neuter, model=model, slate_date=slate_date, removals=removals)
  picks = prepared[0]
  picks['team_proj'] = picks.groupby(level=0)['actual'].sum()
  picks['team_+/-'] = picks.groupby(level=0)['proj_proj+/-'].sum()
  #trying to identify salary arbitrage against dkz
  picks['team_dk_salary'] = picks.groupby(level=0)['dkSalary'].sum()
  stats = prepared[1]
  player_list = pd.DataFrame(picks.groupby(level=0).apply(lambda x: x['RylandID'].tolist()))
  player_list[1] = player_list[0].apply(lambda x: x[0])
  player_list[2] = player_list[0].apply(lambda x: x[1])
  player_list[3] = player_list[0].apply(lambda x: x[2])
  player_list[4] = player_list[0].apply(lambda x: x[3])
  player_list[5] = player_list[0].apply(lambda x: x[4])
  player_list[6] = player_list[0].apply(lambda x: x[5])
  player_list[7] = player_list[0].apply(lambda x: x[6])
  player_list[8] = player_list[0].apply(lambda x: x[7])
  player_list[9] = player_list[0].apply(lambda x: x[8])
  player_list.drop(0,axis=1, inplace=True)
  picks = picks.join(player_list)

  picks = picks.reset_index().set_index('name').reset_index(drop=True).sort_values(by='lineup').set_index('lineup')

  user = os.getlogin()
  path = "C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\ml_predictions\\{1}\\".format(user, slate_date)
  teams = picks.groupby(level=0).first()
  teams = teams.sort_values(by='proba_1', ascending=False).iloc[:optimization_pool]
  optimaldf = fantasyze_proj(slate_date=slate_date) 
  teams=teams[teams['team_proj']>=optimaldf['actual'].sum()*pct_from_opt_proj]
  teams=teams[teams['team_dk_salary']>=dksalary_min]
  teams.sort_values(by='proba_1', ascending=False).to_csv(path+'optimtkttemp.csv')
  
  #prepare ownership parameters
  owndict = stats['proj_proj+/-'].to_dict() #right now this is just to get all players names 
  own_limits = []
  for i in owndict.keys():
    entry = ["{0}".format(i), int(-1), int(roster_size*max_pct_own)]
    own_limits.append(entry)

  team = run(roster_size=roster_size, own_limits=own_limits, slate_date=slate_date)
  players = team.players
  ids = [i.lineup for i in players]

  fanduel_ticket_optimized(slate_date=slate_date, ids=ids, model=model)
      
  print("--- %s seconds ---" % (time.time() - start_time))

  return team.__repr__





    
    






























# %%
