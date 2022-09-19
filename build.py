import os
import math
import numpy as np
import pandas as pd

from _historical.optimize.optimize import fantasyze
from _predict.optimize.optimize import fantasyze_live
from _historical.feature_generation.frv1 import buildml
from _predict.feature_generation.frv1 import buildml_live
from multiprocessing import Pool
from itertools import repeat

from config import curr_historical_optimize_weeks, master_historical_weeks



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
    

# cores = 30
# names = [f[:-7] for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
# weeks_available = len(names)
# weeks_core = math.ceil(len(names)/cores)
# week_ranges = np.arange(0,weeks_available+weeks_core,weeks_core)
# ranges = [names[week_ranges[i]:week_ranges[i+1]] for i in np.arange(
#         len(week_ranges)-1)]
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
pool.starmap(fantasyze_live, zip(workers, repeat('9.14.22')))
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
teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])
preds = pd.read_csv(path + 'predictions.csv').sort_values(by='lineup',ascending=False).drop_duplicates('prediction',keep='first')

picks = preds[['lineup', 'whose_in_flex', 'prediction']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
picks.sort_values(by='prediction', ascending=False, inplace=True)

ticket = picks.iloc[:9000]


remove = ['80468-69213', '80468-42104', '80468-89981', '80468-94094', '80468-86192'] #86192 is hamler 
tests = []
for i in ticket.index.unique():
  ticket_cols = ['QB','RB','RB','WR','WR','WR','TE','FLEX','DEF']
  test = ticket.loc[i][['pos','Id','whose_in_flex','prediction']].sort_values('Id')
  id2 = sorted(test['Id'].values)
  injury = len(list(set(id2).intersection(set(remove))))
  proj = test['prediction'].iloc[0]
  flex = test['whose_in_flex'].iloc[0]
  test = test[['pos','Id']].sort_values('pos')
  test.set_index('pos', inplace=True)
  test.index = np.where(test.index=='D', 'DEF', test.index)
  flex_pull = test[test.index==flex].iloc[0,0]
  test.index = np.where(test['Id']==flex_pull, 'FLEX', test.index)
  test = test.loc[ticket_cols].drop_duplicates('Id').T
  test['id2'] = str(id2)
  test['prediction'] = proj
  test['injury'] = injury
  tests.append(test)
upload = pd.concat(tests)
upload = upload[upload['injury']==0].sort_values(by='prediction', ascending=False).drop_duplicates('id2',keep='first')
upload.iloc[:140,:-2].to_csv(path+'ticket.csv')







