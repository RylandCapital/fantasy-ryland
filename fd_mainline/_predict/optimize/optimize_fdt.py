import os
import numpy as np
import pandas as pd
import time
import csv

from ortools.linear_solver import pywraplp

from fd_mainline._fantasyml import neuterPredictions

from fd_mainline.config import gameday_week

from fd_mainline._predict.player_stats.helpers import fanduel_ticket_optimized

import statistics

'''dont forget to add times to stats file'''


def prepare(model='ensemble', neuter=False, slate_date=''):

  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
  path2 = 'C:\\Users\\{0}\\.fantasy-ryland\\model_tracking\\teams\\{1}\\'.format(user,slate_date)
  path3 = os.getcwd() + r"\fd_mainline\_predict\player_stats\by_week"

  predictions = pd.read_csv(path+'model_tracking\\predictions\\{0}_{1}.csv'.format(slate_date, model))
  predictions = predictions.sort_values(by='lineup',ascending=False) 

  onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
  teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

  stats = pd.read_csv(path3 + "\\" + '{0}.csv'.format(gameday_week)) 
  stats = stats.set_index('RylandID_master')

  teams = teams[teams['lineup'].isin(predictions['lineup'].unique())]
  teams = teams.set_index('name').join(stats, how='outer', lsuffix='_ot').reset_index()

  if neuter==True:
      nps = neuterPredictions(1, predictions)[['lineup','proba_1_neutralized']].set_index('lineup')
      predictions = predictions.set_index('lineup').join(nps)
      predictions.reset_index(inplace=True)
      predictions['proba_1'] = predictions['proba_1_neutralized']
      predictions.drop(['proba_1_neutralized'], axis=1, inplace=True)

  onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
  teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])


  ##
  stats = pd.read_csv(path3 + "\\" + '{0}.csv'.format(gameday_week)) 
  stats = stats.set_index('RylandID_master')
  ##

  picks = predictions[['lineup', 'whose_in_flex', 'proba_1']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
  picks['proba_rank'] = picks['proba_1'].rank(method='max', ascending=False)/9


  picks.sort_values(by='proba_1', ascending=False, inplace=True)

  return picks, stats

class Player:
  def __init__(self, opts):
    self.proba1 = round(float(opts['proba_1']),4)
    self.rank = int(float(opts['proba_rank']))
    self.lineup = str(opts['lineup'])
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
    self.time = round(float(opts['time']),4)
    self.lock = False
    self.ban = False
    

  def __repr__(self):
    return "[{0},{1},{2}]".format(self.proba1,self.rank,self.lineup)
                                    
class Roster:

  POSITION_ORDER = {
    "TEAM": 1,
  }

  def __init__(self):
    self.players = []

  def add_player(self, player):
    self.players.append(player)
  
  def actual(self):
     return sum(map(lambda x: x.proba1, self.players))
    
  def mean_actual(self):
     return statistics.mean(map(lambda x: x.proba1, self.players))

  def time(self):
     return sum(map(lambda x: x.time, self.players))
  
  def mean_time(self):
     return statistics.mean(map(lambda x: x.time, self.players))

  def __repr__(self):
    s = "Actual Proba1: %s" % self.actual()
    s += "\nMean Proba1: %s" % self.mean_actual()
    s += "\n\nTime Total: %s" % self.time()
    s += "\nMean Time: %s" % self.mean_time()
    return s

def run(roster_size=150, own_limits=''):

  solver = pywraplp.Solver('FD', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  all_players = []  
  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)

  with open(path+ r'optimize_pred_file.csv', 'r') as csvfile:
    csvdata = csv.DictReader(csvfile, skipinitialspace=True)
    for row in csvdata:
      all_players.append(Player(row))

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

    for i, player in enumerate(all_players):
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

def slate_optimization(slate_date='12.7.22', model='ensemble', roster_size=150, average_time=0, minimum_player_projown=-1, small_slate=False, optimization_pool=int(50000), neuter=False):

  start_time = time.time()
  print('initiating dfs calculations''')

  #prepare ticket optimization file
  prepared = prepare(neuter=neuter, model=model, slate_date=slate_date)
  picks = prepared[0]
  stats = prepared[1]
  player_list = pd.DataFrame(picks.groupby(level=0).apply(lambda x: x['name'].tolist()))
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

  picks = picks.reset_index().set_index('name').join(stats['time']).reset_index(drop=True).sort_values(by='lineup').set_index('lineup')
  times = picks.groupby(level=0)['time'].mean()

  #add average start times for optimizer
  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
  teams = picks.drop('time', axis=1).groupby(level=0).first().join(times)

  #toggle average starting time for teams if you want 4PM heavy
  #2.3 or higher is atleast 4/9 players starting at 4PM - 2.0 would be three or more 
  teams = teams[teams['time']>average_time]

  #write file to folder
  teams.sort_values(by='proba_1', ascending=False).iloc[:optimization_pool].to_csv(path+'optimize_pred_file.csv')

  #prepare ownership parameters
  owndict = stats['proj_own'].to_dict()
  own_limits = []
  if small_slate==False:
    for i in owndict.keys():
      if (owndict[i]/100)<minimum_player_projown:
        entry = ["{0}".format(i), int(-1), int(0)]
      else:
        entry = ["{0}".format(i), int(((owndict[i]/100)/2)*roster_size)-1, int(((owndict[i]/100)*2)*roster_size)]
      own_limits.append(entry)
  if small_slate==True:
    for i in owndict.keys():
      print(owndict[i]/100)
      if (owndict[i]/100)<minimum_player_projown:
        entry = ["{0}".format(i), int(-1), int(0)]
      else:
        entry = ["{0}".format(i), int(-1), int(roster_size)]
      own_limits.append(entry)
    
      
  team = run(roster_size=roster_size, own_limits=own_limits)
  players = team.players
  ids = [i.lineup for i in players]
  probas = [i.proba1 for i in players]
  ranks = [i.rank for i in players]

  fanduel_ticket_optimized(slate_date=slate_date, ids=ids, removals=[], model='ensemble')
      
  print("--- %s seconds ---" % (time.time() - start_time))





    
    






























# %%
