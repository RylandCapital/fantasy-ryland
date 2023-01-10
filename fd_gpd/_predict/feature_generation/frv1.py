import pandas as pd
import numpy as np
import time
import traceback
import os

from fd_gpd.config import gameday_week

'''1) pull all hisotrical teams from the database created from the optimizer'''
user = os.getlogin()
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live_gpd\\'.format(user)
mypath2 = os.getcwd() + r"\fd_gpd\_predict\player_stats\by_week"

def buildml_live(strdates):

    '''3) Calculate Features'''
#%%  
    for datee in strdates:
        try:
                
            start_time = time.time()
            
            print('initiating dfs calculations''')   
            
            #read in compressed file
            file = pd.read_csv(mypath + str(datee) + '.csv.gz',
                               compression='gzip').sort_values('lineup')

            stats = pd.read_csv(mypath2 + "\\" + '{0}.csv'.format(gameday_week)) 
            stats = stats.set_index('RylandID_master')
          
            file = file.set_index('name').join(stats, how='outer', lsuffix='_ot').reset_index()

            try:
                file.drop('Position', axis=1, inplace=True)
            except:
                pass
            try:       
                 file.rename(columns={'pos':'Position'}, inplace=True)
            except:
                pass
            
            
            #edits
            #file = file[sorted(file.columns.tolist())]
            print('....data recieved')
            
            
            file = file.dropna(subset=['lineup'])
            
            file['games'] = (file['team_team'] + file['opp']).str.replace(
                    '@', '').str.split('')

            file['games2'] = (file['team_team'] + '_' + file['opp']).str.replace('@','').str.split('_')

            file['opp'] = file['opp'].str.replace('@', '')
            file['games'] = file['games'].apply(lambda x: sorted(x))
            file['games'] = file['games'].apply(lambda x: ''.join(x))
            file['slot'] = file.groupby(['lineup', 'position'])['salary'].rank(
                    method='max',ascending=False)
            file['slot'] = file['Position'] + file['slot'].astype(int).astype(str)

            
        
            lineups = file.groupby('lineup')
            teamstackgroup = file.groupby(['lineup', 'team_team'])
            
            lencheck = lineups.apply(lambda x: len(x)).value_counts()
            if (lencheck.index[0]==9) & (len(lencheck)==9):
                raise NameError('Team Lengths Not All 9')
                
            
            team_means = lineups[
                'proj_proj',
                'proj_ceiling',
                'proj_floor',
                'proj_pts/sal',
                'proj_proj+/-', 
                'vegas_pts', 
                'vegas_o/u',
                'trends_opp+/-', 
                'vegas_ml',
                'vegas_opppts', 
                'fantasymonth_ppg',
                'lines_full',
                'lines_pp',
                'time_rest',
                'time_b2b',
                'fantasymonth_consistency',
                'stats-month_corsifor',
                'stats-month_s+blk',
                'stats-month_s',
                'stats-15_corsifor',
                'stats-15_s+blk',
                'stats-15_s',
                'stats-15_blk',
                'stats-15_satt',
                'stats-15_ppsatt',
                'stats-15_toi',
                'stats-15_pptoi',
                'stats-15_ppg',
                'stats-15_ppa', 
                'teamstats-month_oppg',
                'teamstats-month_opps',
                'teamstats-month_pks',
                'teamstats-month_pk%',
                'teamstats-month_opppps',
                'teamstats-month_opppp%'          
                ].mean()
            team_means.columns = [i+'_mean' for i in team_means.columns]

            team_stds = lineups[
                'proj_proj',
                'proj_ceiling',
                'proj_floor',
                'proj_pts/sal',
                'proj_proj+/-', 
                'vegas_pts', 
                'vegas_o/u',
                'trends_opp+/-', 
                'vegas_ml',
                'vegas_opppts', 
                'fantasymonth_ppg',
                'lines_full',
                'lines_pp',
                'time_rest',
                'time_b2b',
                'fantasymonth_consistency',
                'stats-month_corsifor',
                'stats-month_s+blk',
                'stats-month_s',
                'stats-15_corsifor',
                'stats-15_s+blk',
                'stats-15_s',
                'stats-15_blk',
                'stats-15_satt',
                'stats-15_ppsatt',
                'stats-15_toi',
                'stats-15_pptoi',
                'stats-15_ppg',
                'stats-15_ppa', 
                'teamstats-month_oppg',
                'teamstats-month_opps',
                'teamstats-month_pks',
                'teamstats-month_pk%',
                'teamstats-month_opppps',
                'teamstats-month_opppp%'          
                ].std()
            team_stds.columns = [i+'_std' for i in team_stds.columns]
        
      
            
            sal_std = lineups['salary'].std()/file.drop_duplicates(subset=['name',
                         'proj_proj'], keep='first')['salary'].std()
            
            plyrs_eq_0 = lineups.apply(lambda x: len(x[x['salary']==3000]))
            plyrs_0= lineups.apply(lambda x: len(x[x['salary']<3500]))
            plyrs_less_5 = lineups.apply(lambda x: len(x[x['salary']<4500]))
            plyrs_less_10 = lineups.apply(lambda x: len(x[x['salary']<5200]))
            plyrs_less_25 = lineups.apply(lambda x: len(x[x['salary']<8500]))
            plyrs_abv_90 = lineups.apply(lambda x: len(x[x['salary']>9500]))
            plyrs_abv_99 = lineups.apply(lambda x: len(x[x['salary']>=10000]))
            max_salary = file['salary'].max()
            plyrs_eq_1 = lineups.apply(lambda x: len(x[x['salary']==max_salary]))
            
            
            '''GAMES TEAM INFO'''
            maxplayersfrom1team = lineups.apply(
                    lambda x: x['team_team'].value_counts().iloc[0])
            num_games_represented = lineups.apply(
                    lambda x: len(x['games'].unique()))
           
        
            #part 1 (agg the game stack stat)
            numberofgamestacks = lineups.apply(lambda x: len(x['games'].value_counts()[
                    x['games'].value_counts()>1].index.values))
            
            '''TEAM STACKS'''
            print('building teamStack analysis')
            #part 1 (agg the game stack stat)
            numberofteamstacks = lineups.apply(lambda x: len(x['team_team'].value_counts()[
                    x['team_team'].value_counts()>1].index.values))
            
            team_stack_strings = teamstackgroup.apply(
                    lambda x: x['slot'].tolist() if len(x)>1
                    else [])
            
            team_stack_salaries = teamstackgroup.apply(
                    lambda x: x['salary'].sum()/len(x) if len(x)>1
                    else 0) 
            
            team_stack_ou = teamstackgroup.apply(
                    lambda x: x['vegas_o/u'].sum()/len(x) if len(x)>1
                    else 0)

            team_stack_pts = teamstackgroup.apply(
                    lambda x: x['vegas_pts'].sum()/len(x) if len(x)>1
                    else 0)
        
            team_stack_ml = teamstackgroup.apply(
                    lambda x: x['vegas_ml'].sum()/len(x) if len(x)>1
                    else 0)

            teamstackdf = pd.DataFrame(team_stack_strings).join(
                    pd.DataFrame(team_stack_salaries), rsuffix='_salary').join(
                    pd.DataFrame(team_stack_ou)).join(
                    pd.DataFrame(team_stack_pts), rsuffix='_pts').join(
                    pd.DataFrame(team_stack_ml), rsuffix='_ml')  
            teamstackdf.columns = ['0', '0_salary', 0, 'pts', 'ml']
                        

            teamstackdf['0'] = teamstackdf['0'].apply(lambda x: ''.join(
                    sorted(x)) if len(x)>1 else 0)

            teamstackdf = teamstackdf.sort_values(['lineup','0_salary'],
             ascending=[False,False])
                    
                    
            #part 2 (out agged stats into lists sorted by stack string)
            team_stack_strings2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0]['0'] \
                                     .tolist())
            
            team_stack_salaries2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0]['0_salary'] \
                                     .tolist())
            
            team_stack_ou2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0][0] \
                                     .tolist())

            team_stack_pts2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0]['pts'] \
                                     .tolist())
            
            team_stack_ml2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0]['ml'] \
                                     .tolist())
            
            #part 3 create feature column by stack string
            team_stack1 = team_stack_strings2.apply(lambda x: x[0] 
                                                    if len(x)>=1 else 'NA')
            team_stack2 = team_stack_strings2.apply(lambda x: x[1]
                                                    if len(x)>=2 else 'NA')
            team_stack3 = team_stack_strings2.apply(lambda x: x[2] 
                                                    if len(x)>=3 else 'NA')
            team_stack4 = team_stack_strings2.apply(lambda x: x[3] 
                                                    if len(x)==4 else 'NA')
            
            team_stack1salary = team_stack_salaries2.apply(lambda x: x[0]
                                                    if len(x)>=1 else 0)
            team_stack2salary = team_stack_salaries2.apply(lambda x: x[1] 
                                                    if len(x)>=2 else 0)
            team_stack3salary = team_stack_salaries2.apply(lambda x: x[2]
                                                    if len(x)>=3 else 0)
            team_stack4salary = team_stack_salaries2.apply(lambda x: x[3]
                                                    if len(x)==4 else 0)
            
            team_stack1ou = team_stack_ou2.apply(lambda x: x[0]
                                                    if len(x)>=1 else 0)
            team_stack2ou = team_stack_ou2.apply(lambda x: x[1] 
                                                    if len(x)>=2 else 0)
            team_stack3ou = team_stack_ou2.apply(lambda x: x[2]
                                                    if len(x)>=3 else 0)
            team_stack4ou = team_stack_ou2.apply(lambda x: x[3]
                                                    if len(x)==4 else 0)

            team_stack1pts = team_stack_pts2.apply(lambda x: x[0]
                                                    if len(x)>=1 else 0)
            team_stack2pts= team_stack_pts2.apply(lambda x: x[1] 
                                                    if len(x)>=2 else 0)
            team_stack3pts = team_stack_pts2.apply(lambda x: x[2]
                                                    if len(x)>=3 else 0)
            team_stack4pts = team_stack_pts2.apply(lambda x: x[3]
                                                    if len(x)==4 else 0)

            team_stack1ml = team_stack_ml2.apply(lambda x: x[0]
                                                    if len(x)>=1 else 0)
            team_stack2ml= team_stack_ml2.apply(lambda x: x[1] 
                                                    if len(x)>=2 else 0)
            team_stack3ml = team_stack_ml2.apply(lambda x: x[2]
                                                    if len(x)>=3 else 0)
            team_stack4ml = team_stack_ml2.apply(lambda x: x[3]
                                                    if len(x)==4 else 0)


            position_numbers = lineups['Position'].value_counts()
            cnumbers = position_numbers.loc[:,'C',:]
            wnumbers = position_numbers.loc[:,'W',:]
            defnumbers = position_numbers.loc[:,'D',:]

            min_salary = lineups['salary'].min()
            min_proj = lineups['proj_proj'].min()
            min_ptssal = lineups['proj_pts/sal'].min()

            max_salary = lineups['salary'].max()
            max_proj = lineups['proj_proj'].max() 
            max_ptssal = lineups['proj_pts/sal'].max()

            
            analysis = pd.concat([
                                  team_means,
                                  team_stds,
                                  sal_std,
                                  plyrs_eq_0,
                                  plyrs_0,
                                  plyrs_less_5,
                                  plyrs_less_10,
                                  plyrs_less_25,
                                  plyrs_abv_90,
                                  plyrs_abv_99,
                                  plyrs_eq_1, 
                                  maxplayersfrom1team,
                                  num_games_represented,
                                  numberofgamestacks,
                                  numberofteamstacks,
                                  team_stack1salary,
                                  team_stack2salary,
                                  team_stack3salary, 
                                  team_stack4salary,
                                  team_stack1ou,
                                  team_stack2ou,
                                  team_stack3ou,
                                  team_stack4ou,
                                  team_stack1pts,
                                  team_stack2pts,
                                  team_stack3pts,
                                  team_stack4pts,
                                  team_stack1ml,
                                  team_stack2ml,
                                  team_stack3ml,
                                  team_stack4ml,
                                  cnumbers,
                                  wnumbers,
                                  defnumbers,
                                  min_salary,
                                  min_proj,
                                  min_ptssal,
                                  max_salary,
                                  max_proj,
                                  max_ptssal,
                                  team_stack1,
                                  team_stack2,
                                  team_stack3,
                                  team_stack4,
                                                             
                                ], axis=1)
             
            analysis.columns =  \
                        team_means.columns.tolist() + \
                        team_stds.columns.tolist() + \
                        ['salary_std',
                        'plyrs_eq_0',
                        'plyrs_<_0',
                        'plyrs_less_5',
                        'plyrs_less_10',
                        'plyrs_less_25',
                        'plyrs_abv_90',
                        'plyrs_abv_99',
                        'plyrs_eq_1',
                        'maxplayersfrom1team',
                        'num_games_represented',
                        'numberofgamestacks',
                        'numberofteamstacks',
                        'team_stack1salary',
                        'team_stack2salary',
                        'team_stack3salary', 
                        'team_stack4salary',
                        'team_stack1ou',
                        'team_stack2ou',
                        'team_stack3ou',
                        'team_stack4ou',
                        'team_stack1pts',
                        'team_stack2pts',
                        'team_stack3pts',
                        'team_stack4pts',
                        'team_stack1ml',
                        'team_stack2ml',
                        'team_stack3ml',
                        'team_stack4ml',
                        'numberofcenters',
                        'numberofwingers',
                        'numberofdefensemen',
                        'min_salary',
                        'min_proj',
                        'min_ptssal',
                        'max_salary',
                        'max_proj',
                        'max_ptssal',
                        'team_stack1',
                        'team_stack2',
                        'team_stack3',
                        'team_stack4',
                        
                        ]
            analysis.loc[:,'proj_proj_mean':'max_ptssal'] = analysis.loc[:,'proj_proj_mean':'max_ptssal'].rank(pct=True)
            analysis['number_teams_on_slate'] = int(len(file['team_team'].unique())/2) 
            analysis = analysis.reset_index()
            analysis['week'] = datee
            analysis['id'] = analysis['week'].astype(str) + \
            analysis['lineup'].astype(str) 


            analysis.to_csv('C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week_live_gpd\\{1}.csv.gz'.format(user, datee),
                               compression='gzip', index=False)
        except Exception as e:
            print('Caught exception in worker thread (x = {0}):'.format(datee))
        
            # This prints the type, value, and stack trace of the
            # current exception being handled.
            traceback.print_exc()
        
            print()
            raise e
        
        print("--- %s seconds ---" % (time.time() - start_time))

    return True
    

                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# %%
