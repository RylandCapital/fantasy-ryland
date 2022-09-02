import os
import math
import numpy as np

from _historical.optimize.optimize import fantasyze
from _historical.feature_generation.frv1 import buildml
from multiprocessing import Pool

from config import curr_historical_optimize_weeks



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

'''Optimize New Histoical Teams'''
#optimize teams using optimizer. this creates teams from the 
#fantasylabs scrape script. If you want to add an old week to the 
#dataset you have to use scraper on fantasy labs 
weeks = curr_historical_optimize_weeks

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
user = os.getlogin()
          # Specify path
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week\\'.format(user)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    

cores = 30
names = [f[:-7] for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
weeks_available = len(names)
weeks_core = math.ceil(len(names)/cores)
week_ranges = np.arange(0,weeks_available+weeks_core,weeks_core)
ranges = [names[week_ranges[i]:week_ranges[i+1]] for i in np.arange(
        len(week_ranges)-1)]


pool = Pool(processes=cores)
results = pool.map(buildml, ranges)
pool.close()
pool.join() 
################################################
