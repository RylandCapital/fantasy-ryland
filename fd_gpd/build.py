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

from fd_gpd._review.helpers import analyze_gameday_pool_with_ids



from multiprocessing import Pool
from itertools import repeat

from fd_gpd.config import historical_winning_scores, curr_historical_optimize_weeks, master_historical_weeks, gameday_week


################################################
################################################
################################################
'''HISTORICAL TOOLS'''
################################################
################################################
################################################
# dates = list(historical_winning_scores.keys())[35:]
# ids = [historical_winning_scores[i]['slate_id'] for i in dates]
'''pull historical week'''
pull_stats(slate_ids=[50], strdates=['1/14/23'])          


'''Optimize New Training Teams from Raw Data'''
################################################
################################################
'''Create Local Export Env'''
user = os.getlogin()
# Specify path
path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
path2 = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_gpd\\'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path)
  os.mkdir(path+'optimized_teams_by_week_gpd\\')
  os.mkdir(path+'optimized_teams_by_week_live_gpd\\')
  os.mkdir(path+'optimized_ml_by_week_gpd\\')
  os.mkdir(path+'optimized_ml_by_week_live_gpd\\')

if os.path.exists(path2) == False:
  os.mkdir(path2)
  os.mkdir(path+'optimized_teams_by_week_live_gpd\\')
  os.mkdir(path+'optimized_ml_by_week_gpd\\')
  os.mkdir(path+'optimized_ml_by_week_live_gpd\\')

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
path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week_gpd'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path)

'''pull all hisotrical teams from the database created from the optimizer'''

ranges = curr_historical_optimize_weeks

pool = Pool(processes=len(ranges))
results = pool.map(buildml, ranges)
pool.close()
pool.join() 


'''concat all ml files to create master training set'''
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week_gpd\\'.format(user)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
file = pd.concat([pd.read_csv(mypath + f, compression='gzip').sort_values('lineup') for f in onlyfiles])
for i in file.columns:
  try:
    file[i] = file[i].round(4)
  except:
    pass
file.to_csv('C:\\Users\\{0}\\.fantasy-ryland\\mluploadgpd.csv'.format(user))
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
pull_stats_live(slate_ids=['1/17/23'], strdates=['1/17/23'])    


'''Optimize Live Theoretical Teams for Gameday'''
################################################
################################################
'''Create Local Export Env'''
user = os.getlogin()
# Specify path
path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live_gpd'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path+'optimized_teams_by_week_live_gpd\\')

workers = [[i] for i in np.arange(1,35)]

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
path = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week_live_gpd'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path)

'''pull all hisotrical teams from the database created from the optimizer'''
user = os.getlogin()
          # Specify path
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live_gpd\\'.format(user)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    

cores = 35
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
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week_live_gpd\\'.format(user)
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
file = pd.concat([pd.read_csv(mypath + f, compression='gzip').sort_values('lineup') for f in onlyfiles])
for i in file.columns:
  try:
    file[i] = file[i].round(4)
  except:
    pass
file.to_csv('C:\\Users\\{0}\\.fantasy-ryland\\mlupload_livegpd.csv'.format(user))
################################################


'''Optimize Your Slate Using ML Results that you downloaded or saved'''
################################################
################################################
roster = slate_optimization(
  slate_date='1.17.23',
  model='ensemble',
  roster_size=75, 
  opt_proj=151.2,
  pct_from_opt_proj=.85,
  small_slate=False,
  removals = [],
  optimization_pool=int(50000), 
  neuter=False
  )










'''Review'''
################################################
################################################
user = os.getlogin()
path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
model = 'ensemble'
slate = '1.10.23'
historical_id = 48
#how many top model teams do you want to benchmark
ids_file = pd.read_csv(path+'model_tracking\\predictions_gpd\\{0}_{1}_ids.csv'.format(slate,model)).drop_duplicates('lineup').sort_values(by='proba_1', ascending=False).iloc[:150]
dfn, team_scoresn, act_describen, player_pctsn, topn, corrn, duplicatesn, top_proba_scoresn = analyze_gameday_pool_with_ids(
  ids=ids_file['lineup'].tolist(),
  historical_id =historical_id,
  week=slate,
  model=model
  )
top_proba_scoresn.sort_values('proj_actpts')
top_proba_scoresn['proj_actpts'].describe()


#ways to improve team quality when constructing slate
#['plyrs_<_0']<0.4798
#['proj_proj+/-_mean']>0.5

#need to figure out 4 player per team max (test and train pool)


mluploadgpd = pd.read_csv('C:\\Users\\{0}\\.fantasy-ryland\\mluploadgpd.csv'.format(user))
d1 = mluploadgpd.groupby('proj_proj+/-_mean')['ismilly'].sum()
d2 = mluploadgpd.groupby('proj_proj+/-_mean')['ismilly'].apply(lambda x: len(x))
pd.concat([d1,d2],axis=1).to_csv(r'C:\Users\rmathews\Downloads\explore.csv')

mluploadgpd.groupby('trends_opp+/-_mean')['ismilly'].apply(lambda x: x)
mluploadgpd[mluploadgpd['proj_proj+/-_mean']>0.5]

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

