import os
import math
import numpy as np
import pandas as pd

from fd_gpd._historical.player_stats.pull_stats import pull_stats
from fd_gpd._predict.player_stats.pull_stats import pull_stats_live
from fd_gpd._historical.optimize.optimize import fantasyze
from fd_gpd._predict.optimize.optimize import fantasyze_live
from fd_gpd._historical.feature_generation.frv1 import buildml
from fd_gpd._predict.feature_generation.frv1 import buildml_live

from fd_gpd._predict.optimize.optimize_fdt import slate_optimization

from fd_gpd._backtesting.helpers import analyze_gameday_pool_with_ids

from multiprocessing import Pool
from itertools import repeat

from fd_gpd.config import historical_winning_scores, curr_historical_optimize_weeks, master_historical_weeks, user, cores, gameday_week



################################################
################################################
################################################

'''HISTORICAL PIPELINE'''

#scrape data, create theo teams, create ml dataset

################################################
################################################
################################################

'''1. pull historical week/s'''
pull_stats(slate_ids=[60], strdates=['2/21/23'])          

'''2. optimize team from historical raw data'''
weeks = curr_historical_optimize_weeks

'''
code for ALL weeks

dates = list(historical_winning_scores.keys())
weeks = []
for i in np.arange(0,57,2)[:-1]:
  weeks.append([dates[i],dates[i+1]])


'''

pool = Pool(processes=len(weeks))
pool.map(fantasyze, weeks)
pool.close()

'''3. create machine learning dataset for dataiku'''
pool = Pool(processes=len(weeks))
results = pool.map(buildml, weeks)
pool.close()
pool.join() 

mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\_historical\\gpd\\ml_datasets\\'.format(user)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
file = pd.concat([pd.read_csv(mypath + f, compression='gzip').sort_values('lineup') for f in onlyfiles])
for i in file.columns:
  try:
    file[i] = file[i].round(4)
  except:
    pass
file.to_csv('C:\\Users\\{0}\\.fantasy-ryland\\_historical\\gpd\\dataiku_upload.csv'.format(user))
################################################

#%%


################################################
################################################
################################################
'''
GAMEDAY PREDICTION TOOLS

''' 
################################################
################################################
################################################

'''pull live week stats from fantasy labs'''
pull_stats_live(slate_ids=['2/21/23'], strdates=['2/21/23'])    

workers = [[i] for i in np.arange(1,cores)]

pool = Pool(processes=len(workers))
pool.starmap(fantasyze_live, zip(workers, repeat(gameday_week), repeat(True)))
pool.close()
################################################
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\optmized_team_pools\\{1}\\'.format(user,gameday_week)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    
names = [f[:-7] for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
weeks_available = len(names)
weeks_core = math.ceil(len(names)/cores)
week_ranges = np.arange(0,weeks_available+weeks_core,weeks_core)
ranges = [names[week_ranges[i]:week_ranges[i+1]] for i in np.arange(
        len(week_ranges)-1)]

pool = Pool(processes=len(ranges))
results = pool.map(buildml_live, ranges)
pool.close()
pool.join() 

'''concat all ml files to create master team pool'''
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\ml_predictions\\{1}\\'.format(user,gameday_week)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
file = pd.concat([pd.read_csv(mypath + f, compression='gzip').sort_values('lineup') for f in onlyfiles])
for i in file.columns:
  try:
    file[i] = file[i].round(4)
  except:
    pass
file.to_csv('C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\ml_predictions\\{1}\\dataiku_upload.csv'.format(user,gameday_week))
#del old individual files
[os.remove(mypath + "\\" + i) for i in onlyfiles]
################################################



#%%
################################################
################################################
################################################
'''
CONSTRUCT OPTIMAL TICKET TO UPLOAD USING MODEL PROBAS

Based on your contest set:

  chose # of teams (roster_size)
  ban players by fanduel ID, 
  set offered parameters (pct away from optimal projected points, max_pct_own)

''' 
################################################
################################################
################################################
roster = slate_optimization(
  slate_date='2.23.23',
  model='ensemble',
  roster_size=279, 
  pct_from_opt_proj=.75,
  max_pct_own=.382,
  dksalary_min=30000,
  removals = [],
  optimization_pool=int(100000), 
  neuter=False
  )

