import os
import numpy as np
import pandas as pd
import time
import csv

from ortools.linear_solver import pywraplp

from fd_mainline._fantasyml import neuterPredictions




def prepare(model='ensemble', neuter=False):

  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
  path2 = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live\\'.format(user)

  predictions = pd.read_csv(path+'predictions_{0}.csv'.format(model))
  if neuter==True:
      nps = neuterPredictions(1, model)[['lineup','proba_1_neutralized']].set_index('lineup')
      predictions = predictions.set_index('lineup').join(nps)
      predictions.reset_index(inplace=True)
      predictions['proba_1'] = predictions['proba_1_neutralized']
      predictions.drop(['proba_1_neutralized'], axis=1, inplace=True)

  onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
  teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

  picks = predictions[['lineup', 'whose_in_flex', 'proba_1']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
  picks['proba_rank'] = picks['proba_1'].rank(method='max', ascending=False)/9


  picks.sort_values(by='proba_1', ascending=False, inplace=True)

  return picks 


picks = prepare()
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


user = os.getlogin()
path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
teams = picks.groupby(level=0).first()
teams.sort_values(by='proba_1', ascending=False).iloc[:200000].to_csv(path+'optimize_pred_file.csv')


class Player:
  def __init__(self, opts):
    self.proba1 = round(float(opts['proba_1']),4)
    self.rank = int(float(opts['proba_rank']))
    self.lineup = str(opts['lineup'])
    self._1 = opts
    self.pred_owns = []
    self.lock = False
    self.ban = False
    

  def __repr__(self):
    return "{0},{1},{2}".format(self.proba1,self.rank,self.lineup)
                                    
class Roster:

  POSITION_ORDER = {
    "TEAM": 1,
  }

  def __init__(self):
    self.players = []

  def add_player(self, player):
    self.players.append(player)

  def projected(self):
    return sum(map(lambda x: x.proba1, self.players))
  
  def actual(self):
     return sum(map(lambda x: x.proba1, self.players))

  def position_order(self, player):
    return self.POSITION_ORDER['TEAM']

  def sorted_players(self):
    return sorted(self.players, key=self.position_order)

  def __repr__(self):
    s = '\n'.join(str(x) for x in self.sorted_players())
    s += "\n\nActual Proba1: %s" % self.actual()
    return s


POSITION_LIMITS = [
      ["TEAM", 150, 150], 
    ]

ROSTER_SIZE = 150

def run():

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
    variables[i]
    objective.SetCoefficient(variables[i], player.proba1)
    
  # salary_cap = solver.Constraint(SALARY_MIN, SALARY_CAP)
  # for i, player in enumerate(all_players):
  #   salary_cap.SetCoefficient(variables[i], player.salary)
    
  #
  # limit = solver.Constraint(LIMLOW, LIMHIGH)
  # for i, player in enumerate(all_players):
  #   limit.SetCoefficient(variables[i], player.proba1)
    
  size_cap = solver.Constraint(ROSTER_SIZE, ROSTER_SIZE)
  for variable in variables:
    size_cap.SetCoefficient(variable, 1)

  for position, min_limit, max_limit in POSITION_LIMITS:
    position_cap = solver.Constraint(min_limit, max_limit)

    for i, player in enumerate(all_players):
      if position == "TEAM":
        position_cap.SetCoefficient(variables[i], 1)

  

  solution = solver.Solve()

  if solution == solver.OPTIMAL:
    roster = Roster()

    for i, player in enumerate(all_players):
      if variables[i].solution_value() == 1:
        roster.add_player(player)

#    print("Optimal roster for: $%s\n" % SALARY_CAP)
#    print(roster)

  else:
    print("No solution :(")
    
  return roster


#%%
start_time = time.time()
print('initiating dfs calculations''')  
    
def fantasyze_live(ws, week, teamstacks_only=True):
  team = run().players
                
  print("--- %s seconds ---" % (time.time() - start_time))

  # user = os.getlogin()
  # # Specify path
  # path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live\\'.format(user)

  # # masterf.to_csv(path+'{0}_{1}.csv.gz'.format(week,w),compression='gzip', index=True)
  
  # print("--- %s seconds ---" % (time.time() - start_time))




    
    






























# %%
