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
pull_stats(slate_ids=[55,56,57], strdates=['1/26/23','2/7/23','2/9/23'])          

'''2. optimize team from historical raw data'''
weeks = curr_historical_optimize_weeks

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
pull_stats_live(slate_ids=['2/17/23'], strdates=['2/17/23'])    

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
  slate_date='2.17.23',
  model='ensemble',
  roster_size=150, 
  pct_from_opt_proj=0,
  max_pct_own= .34,
  removals = [],
  optimization_pool=int(50000), 
  neuter=False
  )



# '''Review'''
# ################################################
# ################################################
# user = os.getlogin()
# path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
# model = 'ensemble'
# slate = '1.10.23'
# historical_id = 48
# #how many top model teams do you want to benchmark
# ids_file = pd.read_csv(path+'model_tracking\\predictions_gpd\\{0}_{1}_ids.csv'.format(slate,model)).drop_duplicates('lineup').sort_values(by='proba_1', ascending=False).iloc[:150]
# dfn, team_scoresn, act_describen, player_pctsn, topn, corrn, duplicatesn, top_proba_scoresn = analyze_gameday_pool_with_ids(
#   ids=ids_file['lineup'].tolist(),
#   historical_id =historical_id,
#   week=slate,
#   model=model
#   )
# top_proba_scoresn.sort_values('proj_actpts')
# top_proba_scoresn['proj_actpts'].describe()


# #ways to improve team quality when constructing slate
# #['plyrs_<_0']<0.4798
# #['proj_proj+/-_mean']>0.5

# #need to figure out 4 player per team max (test and train pool)


# mluploadgpd = pd.read_csv('C:\\Users\\{0}\\.fantasy-ryland\\mluploadgpd.csv'.format(user))
# d1 = mluploadgpd.groupby('proj_proj+/-_mean')['ismilly'].sum()
# d2 = mluploadgpd.groupby('proj_proj+/-_mean')['ismilly'].apply(lambda x: len(x))
# pd.concat([d1,d2],axis=1).to_csv(r'C:\Users\rmathews\Downloads\explore.csv')

# mluploadgpd.groupby('trends_opp+/-_mean')['ismilly'].apply(lambda x: x)
# mluploadgpd[mluploadgpd['proj_proj+/-_mean']>0.5]

# # df = pd.read_csv(r'C:\Users\rmathews\Downloads\mlupload_scored.csv')
# # df = df[df['week']>41]
# # df['prediction'] = np.where(df['proba_1']>.45,1,0)
# # df['correct'] = np.where((df['prediction']==1) & (df['ismilly']==1),1,0)
# # df.groupby('week')['correct'].value_counts()

# # xdf = pd.DataFrame([], columns=['week', 'corrects', 'top_correct_proba', 'ticket_spot'])
# # for i in df['week'].unique():
# #   temp = df[df['week']==i].sort_values(by='proba_1', ascending=False)
# #   temp.reset_index(drop=True, inplace=True)
# #   posdf = temp[temp['correct']==1]
# #   xdf.loc[i,'week'] = i
# #   xdf.loc[i,'correct'] = len(posdf)
# #   try:
# #     xdf.loc[i,'top_correct_proba'] = posdf.iloc[0]['proba_1']
# #     xdf.loc[i,'ticket_spot'] = posdf.index[0]
# #   except:
# #     xdf.loc[i,'top_correct_proba'] = -1
# #     xdf.loc[i,'ticket_spot'] = -1

# # xdf.to_csv(r'C:\Users\rmathews\Downloads\analysis.csv')

