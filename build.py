import os
import math
import numpy as np
import pandas as pd

from _historical.optimize.optimize import fantasyze
from _predict.optimize.optimize import fantasyze_live

from _historical.player_stats.pull_stats import pull_stats
from _predict.player_stats.pull_stats import pull_stats_live

from _historical.feature_generation.frv1 import buildml
from _predict.feature_generation.frv1 import buildml_live

from _predict.player_stats.helpers import fanduel_ticket

from multiprocessing import Pool
from itertools import repeat

from config import curr_historical_optimize_weeks, master_historical_weeks, gameday_week




################################################
################################################
################################################
'''HISTORICAL TOOLS'''
################################################
################################################
################################################

'''pull historical week'''
pull_stats(weeks=[46,47], strdates=['9/7/22', '9/14/22'])         


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
weeks = master_historical_weeks

pool = Pool(processes=len(weeks))
pool.map(fantasyze, weeks)
pool.close()
################################################

#%%
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

ranges = master_historical_weeks

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




################################################
################################################
################################################
'''GAMEDAY PREDICTION TOOLS'''
################################################
################################################
################################################

'''pull live week stats from fantasy labs'''
pull_stats_live(weeks=['9/21/22'], strdates=['9/21/22'])    


'''Optimize Live Theoretical Teams for Gameday'''
################################################
################################################
'''Create Local Export Env'''
user = os.getlogin()
# Specify path
path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path+'optimized_teams_by_week_live\\')

workers = [[i] for i in np.arange(1,40)]

pool = Pool(processes=len(workers))
pool.starmap(fantasyze_live, zip(workers, repeat('9.14.22'), repeat(True)))
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
    

cores = 40
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


'''concat all ml files to create master training set'''
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week_live\\'.format(user)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
file = pd.concat([pd.read_csv(mypath + f, compression='gzip').sort_values('lineup') for f in onlyfiles])
file.to_csv('C:\\Users\\{0}\\.fantasy-ryland\\mlupload_live.csv'.format(user))
################################################



'''after live teams have been uploaded to dataiku and 
predicted and the file has been dropped into 
'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user).
this block brings in the predictions to create 
upload ticket'''
################################################
################################################
user = os.getlogin()
path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
path2 = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live\\'.format(user)

onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
onlyfiles = [f for f in onlyfiles if f.split('_')[0] == gameday_week]
teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

preds = pd.read_csv(path + 'predictions.csv').sort_values(by='lineup',ascending=False).drop_duplicates('prediction',keep='first')

ticket = fanduel_ticket(preds, teams, entries=150, injuries=[])




