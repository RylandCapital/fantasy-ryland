import os
import numpy as np
import pandas as pd
import time
import csv

from ortools.linear_solver import pywraplp
from fd_mainline.config import historical_winning_scores



class Player:
  def __init__(self, opts):
    self.name = opts['RylandID_master']
    self.position = opts['pos'].upper()
    self.salary = int(float((opts['salary'])))
    self.theo_actual = float(np.random.randint(-300,300)) 
    self.actual = float(opts['act_pts'])
    self.plusminus = float(opts['proj+-'])
    self.proj = float(opts['proj'])
    self.team = str(opts['team'])
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
    "QB": 0,
    "RB": 1,
    "WR": 2,
    "TE": 3,
    "D": 4,
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
      ["QB", 1, 1], 
      ["RB", 2, 3],
      ["WR", 3, 4],
      ["TE", 1, 2],
      ["D", 1, 1]
    ]

ROSTER_SIZE = 9

def run(SALARY_CAP, SALARY_MIN, CUR_WEEK, LIMLOW, LIMHIGH):
  solver = pywraplp.Solver('FD', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  all_players = []  
  with open(os.getcwd() + r"\fd_mainline\_historical\player_stats\by_week\{0}.csv".format(str(CUR_WEEK)), 'r') as csvfile:
    csvdata = csv.DictReader(csvfile, skipinitialspace=True)
   
    for row in csvdata:
        test = Player(row)
        if (test.actual > -5):
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
    objective.SetCoefficient(variables[i], player.theo_actual)
    
  
  salary_cap = solver.Constraint(SALARY_MIN, SALARY_CAP)
  for i, player in enumerate(all_players):
    salary_cap.SetCoefficient(variables[i], player.salary)
    
  #
  limit = solver.Constraint(LIMLOW, LIMHIGH)
  for i, player in enumerate(all_players):
    limit.SetCoefficient(variables[i], player.actual)
    
    
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

#    print("Optimal roster for: $%s\n" % SALARY_CAP)
#    print(roster)

  else:
    print("No solution :(")
    
  return roster


#%%
start_time = time.time()
print('initiating dfs calculations''')  

milly_winners_dict = historical_winning_scores
def fantasyze_review(ws, week, teamstacks_only=True):
  for w in ws:
          dfs = [] 
          count=0
          milly = milly_winners_dict[str((w))]
          dupdf = pd.DataFrame([], columns = ['id'])
          dfs = [] 

          i = 0
          while i < 501:
              
              team = run(60000, 50000, w, milly, 500).players
              #######
                
              names = [i.name for i in team]
              actual = [i.actual for i in team]
              position = [i.position for i in team]
              salary = [i.salary for i in team]
              pm = [i.plusminus for i in team]
              proj = [i.proj for i in team]
              
              actual_sum = sum(actual)
              proj_sum = sum(proj)
              pm_sum = sum(pm)

              team_exposures = [i.team for i in team]
              opps = [i.opp.replace('@','') for i in team]
              isteamstack = len([x for x in team_exposures if team_exposures.count(x) >= 2])
                
              df = pd.DataFrame([names, proj, actual, pm, position, salary, team_exposures], index = ['name',
                                  'proj', 'actual', 'plusminus', 'position', 'salary', 'teamz']).T
              df['team_actual'] = actual_sum
              df['team_proj'] = proj_sum
              df['team_pm'] = pm_sum
              df['id'] = ''.join(sorted(''.join(names)))
              df['lineup'] = str(i) + str(0) +'_milly'

              dupdf.loc[i,'id'] = ''.join(sorted(''.join(names)))
              print('{0}-{1}'.format(w,i))  
              df.drop('teamz', inplace=True, axis=1)
              dfs.append(df)
              i+=1

          masterf = pd.concat(dfs)
          masterf.set_index('id', inplace=True)
          masterf = masterf.reset_index().drop_duplicates('id').reset_index()
          

          print("--- %s seconds ---" % (time.time() - start_time))

          user = os.getlogin()
          # Specify path
          path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live\\'.format(user)

          masterf.to_csv(path+'{0}_{1}.csv.gz'.format(week,w),compression='gzip', index=True)
          
          print("--- %s seconds ---" % (time.time() - start_time))



    
    






























# %%
