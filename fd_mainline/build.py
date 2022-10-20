import os
import math
import numpy as np
import pandas as pd

from fd_mainline._historical.optimize.optimize import fantasyze
from fd_mainline._predict.optimize.optimize import fantasyze_live

from fd_mainline._historical.player_stats.pull_stats import pull_stats
from fd_mainline._predict.player_stats.pull_stats import pull_stats_live

from fd_mainline._historical.feature_generation.frv1 import buildml
from fd_mainline._predict.feature_generation.frv1 import buildml_live

from fd_mainline._predict.player_stats.helpers import fanduel_ticket, easy_remove
from fd_mainline._review.helpers import analyze_gameday_pool

from multiprocessing import Pool
from itertools import repeat

from fd_mainline.config import curr_historical_optimize_weeks, master_historical_weeks, gameday_week




################################################
################################################
################################################
'''HISTORICAL TOOLS'''
################################################
################################################
################################################

'''pull historical week'''
pull_stats(weeks=[51], strdates=['10/12/21'])         


'''Optimize New Training Teams from Raw Data'''
################################################
################################################
'''Create Local Export Env'''
user = os.getlogin()
# Specify path
path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path)
  os.mkdir(path+'optimized_teams_by_week\\')
  os.mkdir(path+'optimized_teams_by_week_live\\')
  os.mkdir(path+'optimized_ml_by_week\\')

'''Optimize New Histoical Teams'''
#optimize teams using optimizer. this creates teams from the 
#fantasylabs scrape script. If you want to add an old week to the 
#dataset you have to use scraper on fantasy labs 
weeks = curr_historical_optimize_weeks

pool = Pool(processes=len(weeks))
pool.map(fantasyze, weeks)
pool.close()
################################################


'''Machine Learning Data Prep'''
################################################
################################################
'''Create Local Export Env'''
user = os.getlogin()
# Specify path
path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path)

'''pull all hisotrical teams from the database created from the optimizer'''

ranges = curr_historical_optimize_weeks

pool = Pool(processes=len(ranges))
results = pool.map(buildml, ranges)
pool.close()
pool.join() 


'''concat all ml files to create master training set'''
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week\\'.format(user)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
file = pd.concat([pd.read_csv(mypath + f, compression='gzip').sort_values('lineup') for f in onlyfiles])
file.to_csv('C:\\Users\\{0}\\.fantasy-ryland\\mlupload.csv'.format(user))
################################################

#%%









################################################
################################################
################################################
'''
GAMEDAY PREDICTION TOOLS

CLEAR OUT THESE FOLDERS BEFORE EACH NEW WEEK

'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live'.format(user) and 
'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live\\'.format(user)

''' 
################################################
################################################
################################################

'''pull live week stats from fantasy labs'''
pull_stats_live(weeks=['10/12/22'], strdates=['10/12/22'])    


'''Optimize Live Theoretical Teams for Gameday'''
################################################
################################################
'''Create Local Export Env'''
user = os.getlogin()
# Specify path
path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path+'optimized_teams_by_week_live\\')

workers = [[i] for i in np.arange(1,30)]

pool = Pool(processes=len(workers))
pool.starmap(fantasyze_live, zip(workers, repeat(gameday_week), repeat(True)))
pool.close()
################################################


'''Machine Learning Data Prep LIVE'''
################################################
################################################
'''Create Local Export Env'''
user = os.getlogin()
# Specify path
path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week_live'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path)

'''pull all hisotrical teams from the database created from the optimizer'''
user = os.getlogin()
          # Specify path
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live\\'.format(user)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    

cores = 30
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
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week_live\\'.format(user)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
file = pd.concat([pd.read_csv(mypath + f, compression='gzip').sort_values('lineup') for f in onlyfiles])
file.to_csv('C:\\Users\\{0}\\.fantasy-ryland\\mlupload_live.csv'.format(user))
################################################



'''after live teams have been uploaded to dataiku and 
predictions.csv a file has been dropped into 
'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user).
this block creates upload ticket'''
################################################
################################################
ticket, exposures, stacks = fanduel_ticket(entries=200, max_exposure=75, removals=[], neuter=False)
user = os.getlogin()
path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
exposures.to_csv(path+'exposures.csv')

easy_remove(ids = ['81659-26251','81659-28744','81659-83117', '81659-87770', '81659-60930', '81659-90584'])



'''review'''
df, team_scores, act_describe, player_pcts, top, corr, duplicates, ticket_scores = analyze_gameday_pool(historical_id = 50, week='10.5.22', neuter=False)
dfn, team_scoresn, act_describen, player_pctsn, top, corrn, duplicatesn, ticket_scoresn = analyze_gameday_pool(historical_id = 50, week='10.5.22', neuter=True)