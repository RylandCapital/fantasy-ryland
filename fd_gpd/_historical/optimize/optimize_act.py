import os
import numpy as np
import pandas as pd
import time
import csv

from ortools.linear_solver import pywraplp

class Player:
  def __init__(self, opts):
    self.name = opts['RylandID_master']
    self.position = opts['pos'].upper()
    self.salary = int(float((opts['salary'])))
    self.actual = float(opts['proj_actpts'])
    self.theo_actual = float(np.random.randint(-100,100)) 
    self.plusminus = float(opts['proj_proj+/-'])
    self.proj = float(opts['proj_proj'])
    self.team = str(opts['team_team'])
    self.opp = str(opts['opp'])
    self.lock = False
    self.ban = False

  def __repr__(self):
    return "[{0: <2}] {1: <20}(${2}, {3}) {4}".format(self.position, \
                                    self.name, \
                                    self.salary,
                                    self.actual,
                                    "LOCK" if self.lock else "")
class Roster:
  POSITION_ORDER = {
    "C": 0,
    "W": 1,
    "D": 2,
    "G": 3,
  }

  def __init__(self):
    self.players = []

  def add_player(self, player):
    self.players.append(player)

  def spent(self):
    return sum(map(lambda x: x.salary, self.players)) 

  def projected(self):
    return sum(map(lambda x: x.projected, self.players))
  
  def actual(self):
     return sum(map(lambda x: x.actual, self.players))

  def position_order(self, player):
    return self.POSITION_ORDER[player.position]

  def sorted_players(self):
    return sorted(self.players, key=self.position_order)

  def __repr__(self):
    s = '\n'.join(str(x) for x in self.sorted_players())
    s += "\n\nActual Score: %s" % self.actual()
    s += "\tCost: $%s" % self.spent()
    return s


POSITION_LIMITS = [
      ["C", 2, 4], 
      ["W", 2, 4],
      ["D", 2, 4],
      ["G", 1, 1],
    ]

ROSTER_SIZE = 9

def run(SALARY_CAP, SALARY_MIN, CUR_WEEK):
  solver = pywraplp.Solver('FD', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  all_players = []  
  with open(os.getcwd() + r"\fd_gpd\_historical\player_stats\by_week\{0}.csv".format(str(CUR_WEEK)), 'r') as csvfile:
    csvdata = csv.DictReader(csvfile, skipinitialspace=True)
   
    for row in csvdata:
        test = Player(row)
        if (test.actual > 0):
            all_players.append(Player(row))

  variables = []
  all_players = np.random.choice(all_players, size=int(len(all_players))
      , replace=False)
  for player in all_players:
    if player.lock:
      variables.append(solver.IntVar(1, 1, player.name))
    elif player.ban:
      variables.append(solver.IntVar(0, 0, player.name))
    else:      
      variables.append(solver.IntVar(0, 1, player.name))
    
  objective = solver.Objective()
  objective.SetMaximization()
  
  for i, player in enumerate(all_players):
    objective.SetCoefficient(variables[i], player.actual)
    
  
  salary_cap = solver.Constraint(SALARY_MIN, SALARY_CAP)
  for i, player in enumerate(all_players):
    salary_cap.SetCoefficient(variables[i], player.salary)
     
    
  for position, min_limit, max_limit in POSITION_LIMITS:
    position_cap = solver.Constraint(min_limit, max_limit)

    for i, player in enumerate(all_players):
      if position == player.position:
        position_cap.SetCoefficient(variables[i], 1)

  size_cap = solver.Constraint(ROSTER_SIZE, ROSTER_SIZE)
  for variable in variables:
    size_cap.SetCoefficient(variable, 1)

  solution = solver.Solve()

  if solution == solver.OPTIMAL:
    roster = Roster()

    for i, player in enumerate(all_players):
      if variables[i].solution_value() == 1:
        roster.add_player(player)

  else:
    print("No solution :(")
    
  return roster

#%%
start_time = time.time()
print('initiating dfs calculations''')  
    
def fantasyze_act(hist_slate_id=''):
  
  team = run(55000, 50000, hist_slate_id).players
  #######
  names = [i.name for i in team]
  actual = [i.actual for i in team]
  position = [i.position for i in team]
  salary = [i.salary for i in team]
  
  #settings
  team_exposures = [i.team for i in team]
  
  df = pd.DataFrame([names, actual, position, salary, team_exposures], index = ['name',
                      'actual', 'position', 'salary','teamz']).T
  df['team_salary'] = sum(actual)
  df['lineup'] = 'actual_opitmal' 

  return df

          
               
dfs = []
for i in np.arange(0,67):
  try:
    df = fantasyze_act(hist_slate_id=i)
    df['week_id'] = i
    df = df[['week_id','team_salary']]
    dfs.append(df.iloc[0,:])
  except:
    pass
    




    
    






























# %%
