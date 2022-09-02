import os
import numpy as np
import pandas as pd
import time
import csv

from ortools.linear_solver import pywraplp
from config import historical_winning_scores




class Player:
  def __init__(self, opts):
    self.name = opts['name']
    self.position = opts['pos'].upper()
    self.salary = int(float((opts['salary'])))
    self.theo_actual = float(np.random.randint(1,30)) + float(opts['act_pts'])
    self.actual = float(opts['act_pts'])
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
    return sum(map(lambda x: x.salary, self.players)) + DST_COST

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
  with open(os.getcwd() + r"\_historical\player_stats\by_week\{0}.csv".format(str(CUR_WEEK)), 'r') as csvfile:
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

def fantasyze(ws):
  for w in ws:
      for iters in [0]:
          dfs = [] 
          for i in np.arange(1,5000):
              
              print(i)
              
              if i < 5001:
              #lim low is 90 percent for that week
                  team = run(60000, 59900, w, milly_winners_dict[str((w))]*.9594,
                                                                500).players
                  #######
                    
                  names = [i.name for i in team]
                  actual = [i.actual for i in team]
                  position = [i.position for i in team]
                  salary = [i.salary for i in team]
                  
                  actual_sum = sum(actual)
                    
                  df = pd.DataFrame([names, actual, position, salary], index = ['name',
                                      'actual', 'position', 'salary']).T
                  df['team_salary'] = actual_sum
                  df['week_milly_score'] = ''
                  df['lineup'] = str(i) + str(iters) +'_959'
                    
                  dfs.append(df)
              
              #############################
              if i < 1001:
                  team = run(60000, 59900, w, milly_winners_dict[str((w))]*.9,
                                                                milly_winners_dict[str((w))]*.9594).players
                  #######
                    
                  names = [i.name for i in team]
                  actual = [i.actual for i in team]
                  position = [i.position for i in team]
                  salary = [i.salary for i in team]
                  
                  actual_sum = sum(actual)
                    
                  df = pd.DataFrame([names, actual, position, salary], index = ['name',
                                      'actual', 'position', 'salary']).T
                  df['team_salary'] = actual_sum
                  df['week_milly_score'] = ''
                  df['lineup'] = str(i) +  str(iters) +'_9'
                    
                  dfs.append(df)
              
              #############################
              if i < 2001:
                  team = run(60000, 59900, w, milly_winners_dict[str((w))]*.8,
                                                                milly_winners_dict[str((w))]*.9).players
                  #######
                    
                  names = [i.name for i in team]
                  actual = [i.actual for i in team]
                  position = [i.position for i in team]
                  salary = [i.salary for i in team]
                  
                  actual_sum = sum(actual)
                    
                  df = pd.DataFrame([names, actual, position, salary], index = ['name',
                                      'actual', 'position', 'salary']).T
                  df['team_salary'] = actual_sum
                  df['week_milly_score'] = ''
                  df['lineup'] = str(i) +  str(iters) +'_8'
                    
                  dfs.append(df)
              
              #############################
              if i <3001:
                  team = run(60000, 59900, w, milly_winners_dict[str((w))]*.6,
                                                                milly_winners_dict[str((w))]*.8).players
                  #######
                    
                  names = [i.name for i in team]
                  actual = [i.actual for i in team]
                  position = [i.position for i in team]
                  salary = [i.salary for i in team]
                  
                  actual_sum = sum(actual)
                    
                  df = pd.DataFrame([names, actual, position, salary], index = ['name',
                                      'actual', 'position', 'salary']).T
                  df['team_salary'] = actual_sum
                  df['week_milly_score'] = ''
                  df['lineup'] = str(i) +  str(iters) +'_6'
                    
                  dfs.append(df)
              
              #############################
              if i <4001:
                  team = run(60000, 59900, w, milly_winners_dict[str((w))]*.4 ,
                                                                milly_winners_dict[str((w))]*.6).players
                  #######
                    
                  names = [i.name for i in team]
                  actual = [i.actual for i in team]
                  position = [i.position for i in team]
                  salary = [i.salary for i in team]
                  
                  actual_sum = sum(actual)
                    
                  df = pd.DataFrame([names, actual, position, salary], index = ['name',
                                      'actual', 'position', 'salary']).T
                  df['team_salary'] = actual_sum
                  df['week_milly_score'] = ''
                  df['lineup'] = str(i) +  str(iters) +'_4'
                    
                  dfs.append(df)
              
              #############################
              if i <5001:
                  team = run(60000, 59900, w, milly_winners_dict[str((w))]*.2 ,
                                                                milly_winners_dict[str((w))]*.4).players
                  #######
                    
                  names = [i.name for i in team]
                  actual = [i.actual for i in team]
                  position = [i.position for i in team]
                  salary = [i.salary for i in team]
                  
                  actual_sum = sum(actual)
                    
                  df = pd.DataFrame([names, actual, position, salary], index = ['name',
                                      'actual', 'position', 'salary']).T
                  df['team_salary'] = actual_sum
                  df['week_milly_score'] = ''
                  df['lineup'] = str(i) +  str(iters) +'_2'
                    
                  dfs.append(df)
              
          masterf = pd.concat(dfs)
          masterf = masterf.set_index('name')

          mypath = os.getcwd() + r"\_historical\player_stats\by_week"
          stats = pd.read_csv(mypath + "\\" + '{0}.csv'.format(w)) 
          stats = stats.set_index('name')
          
          masterf = masterf.join(stats, how='outer', lsuffix='_ot')
          features = ['rating', 'salary', 'team', 'opp', 'proj',
                      'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own', 'act_pts',
                      'impld_pts', 'sr', 'buzz', 'leverage', 'pro', 'my', 'bargain',
                      'opp+-', 'snaps', 'pts', 'opppts', 'delta', 'spread', 'o/u',
                      '%rb','%wr', '%te', 'proj_sacks', 'int%', 'bargain',
                      'spread%',  'temp', 'humidity', 'precip%', 'consistency',
                      'pos','rec_trgts%', 'rec_td%', 'rec_yds%', 'rz_opp',
                      'rush_yards%', 'pass_succ', 'rush_succ', 'takeaway%',
                      'lineup', 'week']
          masterf = masterf[features]

          print("--- %s seconds ---" % (time.time() - start_time))

          user = os.getlogin()
          # Specify path
          path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week\\'.format(user)

          masterf.to_csv(path+'{0}.csv.gz'.format(w),compression='gzip', index=True)
          
          print("--- %s seconds ---" % (time.time() - start_time))



    
    





























