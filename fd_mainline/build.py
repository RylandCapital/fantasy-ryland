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

from fd_mainline._review.helpers import analyze_gameday_pool_with_ids
from fd_mainline._review.benchmarking import fantasyze_bench
from fd_mainline._predict.optimize.optimize_fdt import slate_optimization

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
pull_stats(weeks=[60], strdates=['12/14/22'])         


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
pull_stats_live(weeks=['12/21/22'], strdates=['12/21/22'])    


'''Optimize Live Theoretical Teams for Gameday'''
################################################
################################################
'''Create Local Export Env'''
user = os.getlogin()
# Specify path
path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path+'optimized_teams_by_week_live\\')

workers = [[i] for i in np.arange(1,38)]

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








################################################
################################################
################################################
'''
SLATE CONSTUCTION AND REVIEW TOOLS

''' 
################################################
################################################
################################################




'''Optimize Your Slate Using ML Results that you downloaded or saved
('only available from week 14 (12.7.22')'''
################################################
################################################
slate_optimization(
  slate_date='12.14.22',
  model='ensemble',
  roster_size=150, 
  average_time=0, 
  small_slate=False,
  minimum_player_projown=-1,
  optimization_pool=int(50000), 
  neuter=False
  )


'''Review ('only available from week 14 (12.7.22')'''
################################################
################################################
user = os.getlogin()
path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
model = 'ensemble'
slate = '12.14.22'
ids_file = pd.read_csv(path+'model_tracking\\predictions\\{0}_{1}_ids.csv'.format(slate,model)).drop_duplicates('lineup').sort_values(by='proba_1', ascending=False).iloc[:150]
dfn, team_scoresn, act_describen, player_pctsn, topn, corrn, duplicatesn, top_proba_scoresn = analyze_gameday_pool_with_ids(
  ids=ids_file['lineup'].tolist(),
  historical_id = 60,
  week='12.14.22',
  model='ensemble'
  )
top_proba_scoresn.sort_values('act_pts')
top_proba_scoresn['act_pts'].describe()
corrn['act_pts'].corr(corrn['proba_1'])


'''benchmarking again straight optimized teams using projections'''
################################################
################################################
model, bench = fantasyze_bench(
 60,
 live_date='12.14.22',
 number_entries=300, 
 minimum_player_projown=-1, 
 neuter=False, 
 average_time=0, 
 model='ensemble'
 )
























# df = pd.read_csv(r'C:\Users\rmathews\Downloads\mlupload_scored.csv')
# df = df[df['week']>41]
# df['prediction'] = np.where(df['proba_1']>.45,1,0)
# df['correct'] = np.where((df['prediction']==1) & (df['ismilly']==1),1,0)
# df.groupby('week')['correct'].value_counts()

# xdf = pd.DataFrame([], columns=['week', 'corrects', 'top_correct_proba', 'ticket_spot'])
# for i in df['week'].unique():
#   temp = df[df['week']==i].sort_values(by='proba_1', ascending=False)
#   temp.reset_index(drop=True, inplace=True)
#   posdf = temp[temp['correct']==1]
#   xdf.loc[i,'week'] = i
#   xdf.loc[i,'correct'] = len(posdf)
#   try:
#     xdf.loc[i,'top_correct_proba'] = posdf.iloc[0]['proba_1']
#     xdf.loc[i,'ticket_spot'] = posdf.index[0]
#   except:
#     xdf.loc[i,'top_correct_proba'] = -1
#     xdf.loc[i,'ticket_spot'] = -1

# xdf.to_csv(r'C:\Users\rmathews\Downloads\analysis.csv')

