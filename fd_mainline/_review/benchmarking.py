import os
import numpy as np
import pandas as pd
import time
import csv

from ortools.linear_solver import pywraplp


USER = os.getlogin()

class Player:
  def __init__(self, opts):
    self.name = opts['RylandID_master']
    self.position = opts['pos'].upper()
    self.salary = int(float((opts['salary'])))
    self.team = str(opts['team'])
    self.opp = str(opts['opp'])
    self.proj = float(opts['proj'])
    self.act_pts = float(opts['act_pts'])
    self.plusminus = float(opts['proj+-'])
    self.projown = float(opts['proj_own'])
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
        if (test.proj > -5):
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
    objective.SetCoefficient(variables[i], player.proj)
    
  
  salary_cap = solver.Constraint(SALARY_MIN, SALARY_CAP)
  for i, player in enumerate(all_players):
    salary_cap.SetCoefficient(variables[i], player.salary)
    
  #
  limit = solver.Constraint(LIMLOW, LIMHIGH)
  for i, player in enumerate(all_players):
    limit.SetCoefficient(variables[i], player.proj)
    
    
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

def fantasyze_bench(hist_week, live_date='11.30.22', ticket_name=''):
            dfs = [] 
            count=0
            limit=500
            while count < 150:
                
                team = run(60000, 56000, hist_week, 1, limit).players
                #######
                names = [i.name for i in team]
                actual = [i.act_pts for i in team]
                position = [i.position for i in team]
                salary = [i.salary for i in team]
                proj = [i.proj for i in team]
                
                limit = sum(proj)-.01
                #settings
                team_exposures = [i.team for i in team]
                
                df = pd.DataFrame([names, actual, position, salary, proj, team_exposures], index = ['name',
                                    'actual', 'position', 'salary', 'proj', 'teamz']).T
                df['team_salary'] = sum(salary)
                df['lineup'] = 'lineup_' + str(count)  

          
                dfs.append(df)
                count+=1
                print('{0}-{1}'.format(count,limit))
                
            

            masterf = pd.concat(dfs)
            masterf = masterf.set_index('lineup')
            benchmark150 = masterf.groupby(level=0)['actual']


            user = os.getlogin()
            path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
            model = 'ensemble'
            ids_file = pd.read_csv(path+'ids_{0}.csv'.format(model)).drop_duplicates('lineup').sort_values(by='proba_1', ascending=False)

            model_entry_ids = pd.read_csv('C:\\Users\\{0}\\.fantasy-ryland\\{1}.csv'.format(USER, ticket_name))


            # user = os.getlogin()
            # # Specify path
            # path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
            # masterf.to_csv(path+'{0}_{1}.csv'.format(week,w), index=True)
            


    
    





    
    






























# %%
