import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import time
import math
import traceback
import os

from fd_mainline.config import historical_winning_scores



'''1) pull all hisotrical teams from the database created from the optimizer'''
user = os.getlogin()
mypath = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week\\'.format(user)

    
def buildml(ws):

    '''3) Calculate Features'''
#%%  
    for onlyf in ws:
        try:
                
            start_time = time.time()
            
            print('initiating dfs calculations''')   
            
            #read in compressed file
            file = pd.read_csv(mypath + str(onlyf) + '.csv.gz',
                               compression='gzip').sort_values('lineup')
            try:
                file.drop('Position', axis=1, inplace=True)
            except:
                pass
            try:       
                 file.rename(columns={'pos':'Position'}, inplace=True)
            except:
                pass
            
            
            #edits
            file = file[sorted(file.columns.tolist())]
            file['team2'] = np.where(file['team']=='OAK', 'LV', file['team'])
            
            
            print('....data recieved')
            
            
            file = file.dropna(subset=['lineup'])
            
            file['games'] = (file['team'] + file['opp']).str.replace(
                    '@', '').str.split('')

            file['games2'] = (file['team'] + '_' + file['opp']).str.replace('@','').str.split('_')

            file['opp'] = file['opp'].str.replace('@', '')
            file['games'] = file['games'].apply(lambda x: sorted(x))
            file['games'] = file['games'].apply(lambda x: ''.join(x))
            file['slot'] = file.groupby(['lineup', 'Position'])['salary'].rank(
                    method='max',ascending=False)
            file['slot'] = file['Position'] + file['slot'].astype(int).astype(str)
            
        
            lineups = file.groupby('lineup')
            rblineups = file[file['Position'] == 'RB'].groupby('lineup')
            wrlineups = file[file['Position'] == 'WR'].groupby('lineup')
            telineups = file[file['Position'] == 'TE'].groupby('lineup')
            qblineups = file[file['Position'] == 'QB'].groupby('lineup')
            dlineups = file[file['Position'] == 'D'].groupby('lineup')
            nodlineups = file[file['Position'] != 'D'].groupby('lineup')
            gamestacksgroup = file.groupby(['lineup', 'games'])
            teamstackgroup = file.groupby(['lineup', 'team'])
            
            lencheck = lineups.apply(lambda x: len(x)).value_counts()
            if (lencheck.index[0]==9) & (len(lencheck)==9):
                raise NameError('Team Lengths Not All 9')
                
            team_sums = lineups['act_pts','proj','proj_own','proj+-', 'pts', 'o/u',
                                'opp+-', 'snaps','spread', 'pass_succ', 'rush_succ',
                                'takeaway%'].sum()
            team_prods = lineups[['proj_own']].apply(lambda x: (x/100).prod())
        
            rbown = rblineups['proj_own'].sum()
            wrown = wrlineups['proj_own'].sum()
            teown = telineups['proj_own'].sum()
            qbown = qblineups['proj_own'].sum()
            down =  dlineups['proj_own'].sum()
            
            sal_std = lineups['salary'].std()/file.drop_duplicates(subset=['name',
                         'proj'], keep='first')['salary'].std()
            
            plyrs_eq_0= lineups.apply(lambda x: len(x[x['salary']==4000]))
            plyrs_0= lineups.apply(lambda x: len(x[x['salary']<4500]))
            plyrs_less_5 = lineups.apply(lambda x: len(x[x['salary']<5000]))
            plyrs_less_10 = lineups.apply(lambda x: len(x[x['salary']<5200]))
            plyrs_less_25 = lineups.apply(lambda x: len(x[x['salary']<5500]))
            plyrs_abv_90 = lineups.apply(lambda x: len(x[x['salary']>8500]))
            plyrs_abv_99 = lineups.apply(lambda x: len(x[x['salary']>=10000]))
            max_salary = file['salary'].max()
            plyrs_eq_1 = lineups.apply(lambda x: len(x[x['salary']==max_salary]))
            
            '''SLOTS INFORMATION'''
            
            #rb flex
            def flexerror(x, row, extra=[]):
                try:
                    return x.sort_values(by='salary',
                                     ascending=False).iloc[row][slot_cols+extra]
                except:
                    return pd.Series([0]*len(slot_cols+extra),
                                     index = slot_cols+extra)
                    
                
            slot_cols = ['salary', 'snaps','opp+-', 'pts', 'proj', 'proj+-', 'ceil',
                         'spread', 'proj_own', 'team2', 'proj_sacks', 'int%',
                         'bargain', 'leverage', 'opppts']
            
            #rb slots
            rbextras = ['rz_succ%', 'rz_td_pct']
            rbslot1 = rblineups.apply(lambda x: x.sort_values(by='salary',
                                     ascending=False).iloc[0])[slot_cols+rbextras]
            rbslot1.drop(['team2', 'proj_sacks', 'int%'], inplace=True,
                         axis=1)
            
            
            
            rbslot2 = rblineups.apply(lambda x: x.sort_values(by='salary',
                                     ascending=False).iloc[1])[slot_cols+rbextras]
            rbslot2.drop(['team2', 'proj_sacks', 'int%'], inplace=True,
                         axis=1)
            
        
            rbslot3 = rblineups.apply(lambda x: flexerror(x,2,rbextras))
            rbslot3.drop(['team2', 'proj_sacks', 'int%'], inplace=True,
                         axis=1)
            
            
            #wr slots
            wrextras = ['rz_td_pct','rec_yds%','rec_trgts%','rec_td%']
            wrslot1 = wrlineups.apply(lambda x: x.sort_values(by='salary',
                                     ascending=False).iloc[0])[slot_cols+wrextras]
            wrslot1.drop(['team2', 'proj_sacks', 'int%'], inplace=True,
                         axis=1)
            
            
            wrslot2 = wrlineups.apply(lambda x: x.sort_values(by='salary',
                                     ascending=False).iloc[1])[slot_cols+wrextras]
            wrslot2.drop(['team2', 'proj_sacks', 'int%'], inplace=True,
                         axis=1)
            
            
            wrslot3 = wrlineups.apply(lambda x: x.sort_values(by='salary',
                                     ascending=False).iloc[2])[slot_cols+wrextras]
            wrslot3.drop(['team2', 'proj_sacks', 'int%'],
                         inplace=True, axis=1)
            
            
            wrslot4 = wrlineups.apply(lambda x: flexerror(x,3,wrextras))
            wrslot4.drop(['team2', 'proj_sacks', 'int%'], inplace=True,
                         axis=1)
            
            #te slots
            teextras = ['rz_td_pct','rec_yds%','rec_trgts%','rec_td%']
            teslot1 = telineups.apply(lambda x: x.sort_values(by='salary',
                                     ascending=False).iloc[0])[slot_cols+teextras]
            teslot1.drop(['team2', 'proj_sacks', 'int%'], inplace=True,
                         axis=1)
            
            teslot2 = telineups.apply(lambda x: flexerror(x, 1,teextras))
            teslot2.drop(['team2', 'proj_sacks', 'int%'], inplace=True,
                         axis=1)
            
            
            #qb slots
            qbslot1 = qblineups.apply(lambda x: x.sort_values(by='salary',
                                     ascending=False).iloc[0])[slot_cols]
            qbslot1.drop(['team2', 'proj_sacks', 'int%'], inplace=True,
                         axis=1)
            
            #d slots
            dslot1 = dlineups.apply(lambda x: x.sort_values(by='salary',
                                     ascending=False).iloc[0])[slot_cols]
            dslot1.drop('team2', inplace=True, axis=1)
            
            
            '''GAMES TEAM INFO'''
            maxplayersfrom1team = lineups.apply(
                    lambda x: x['team'].value_counts().iloc[0])
            num_games_represented = lineups.apply(
                    lambda x: len(x['games'].unique()))
            opponents = nodlineups.apply(
                    lambda x: x['opp'].tolist())
            defense = dlineups.apply(
                    lambda x: x['team'].tolist())
            off_def_df = pd.DataFrame(opponents, columns=['opp']).join(
                    pd.DataFrame(defense, columns=['team']))
            is_playing_d = off_def_df.apply(lambda row: bool(set(row['team']) & \
                                                             set(row['opp'])), axis=1)
            chalk_players =  lineups.apply(
                    lambda x: len(x[x['proj_own']>=20]))
        
            '''GAME STACKS'''
            print('building gameStack analysis')
            #part 1 (agg the game stack stat)
            numberofgamestacks = lineups.apply(lambda x: len(x['games'].value_counts()[
                    x['games'].value_counts()>1].index.values))
            
            game_stack_strings = gamestacksgroup.apply(
                    lambda x: x['slot'].tolist() if len(x)>1
                    else [])
            
            game_stack_salaries = gamestacksgroup.apply(
                    lambda x: x['salary'].sum()/len(x) if len(x)>1
                    else 0) 
            
            game_stack_ou = gamestacksgroup.apply(
                    lambda x: x['o/u'].sum()/len(x) if len(x)>1
                    else 0)
            
            gamestackdf = pd.DataFrame(game_stack_strings).join(
                    pd.DataFrame(game_stack_salaries), rsuffix='_salary').join \
                    (pd.DataFrame(game_stack_ou)).reset_index()
         

            gamestackdf['0'] = gamestackdf['0'].apply(lambda x: ''.join(
                    sorted(x)) if len(x)>1 else 0)
            
            
            gamestackdf = gamestackdf.sort_values(['lineup','0'])
                    
                    
            #part 2 (out agged stats into lists sorted by stack string)
            game_stack_strings2 = gamestackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0]['0'] \
                                     .tolist())
            
            game_stack_salaries2 = gamestackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0]['0_salary'] \
                                     .tolist())
            
            game_stack_ou2 = gamestackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0][0] 
                                     .tolist())
            
            #part 3 create feature column by stack string
            game_stack1 = game_stack_strings2.apply(lambda x: x[0] 
                                                    if len(x)>=1 else 0)
            game_stack2 = game_stack_strings2.apply(lambda x: x[1]
                                                    if len(x)>=2 else 0)
            game_stack3 = game_stack_strings2.apply(lambda x: x[2] 
                                                    if len(x)>=3 else 0)
            game_stack4 = game_stack_strings2.apply(lambda x: x[3] 
                                                    if len(x)==4 else 0)
            
            game_stack1salary = game_stack_salaries2.apply(lambda x: x[0]
                                                    if len(x)>=1 else 0)
            game_stack2salary = game_stack_salaries2.apply(lambda x: x[1] 
                                                    if len(x)>=2 else 0)
            game_stack3salary = game_stack_salaries2.apply(lambda x: x[2]
                                                    if len(x)>=3 else 0)
            game_stack4salary = game_stack_salaries2.apply(lambda x: x[3]
                                                    if len(x)==4 else 0)
            
            game_stack1ou = game_stack_ou2.apply(lambda x: x[0]
                                                    if len(x)>=1 else 0)
            game_stack2ou = game_stack_ou2.apply(lambda x: x[1] 
                                                    if len(x)>=2 else 0)
            game_stack3ou = game_stack_ou2.apply(lambda x: x[2]
                                                    if len(x)>=3 else 0)
            game_stack4ou = game_stack_ou2.apply(lambda x: x[3]
                                                    if len(x)==4 else 0)
            
         
            '''TEAM STACKS'''
            print('building teamStack analysis')
            #part 1 (agg the game stack stat)
            numberofteamstacks = lineups.apply(lambda x: len(x['team'].value_counts()[
                    x['team'].value_counts()>1].index.values))
            
            team_stack_strings = teamstackgroup.apply(
                    lambda x: x['slot'].tolist() if len(x)>1
                    else [])

            team_stack_game = teamstackgroup.apply(
                    lambda x: x['games'].tolist()[0] if len(x)>1
                    else [])

            team_stack_game_raw = teamstackgroup.apply(
                    lambda x: x['games2'].tolist()[0] if len(x)>0
                    else [])

            
            team_stack_comeback = pd.concat([team_stack_game, team_stack_game_raw, team_stack_strings], axis=1)
            team_stack_comeback['opp'] = team_stack_comeback[1].apply(lambda x: x[1])
            team_stack_comeback['isteamstack'] = team_stack_comeback[2].apply(lambda x: len(x))
            team_stack_comeback['teamtemp'] = team_stack_comeback.index.get_level_values(1)
            lineup_teams = lineups.apply(lambda x: x['team'].tolist())
            lineup_teams.name = 'lineup_teams'
            team_stack_comeback = team_stack_comeback.join(lineup_teams)
            team_stack_comeback['player_opp_same_team'] = team_stack_comeback.groupby(level=[0,1]).apply(
                    lambda x: len(set([x['opp'].iloc[0]]).intersection(x['lineup_teams'].iloc[0])))
            team_stack_comeback['comeback'] = np.where((team_stack_comeback['player_opp_same_team']==1) & (team_stack_comeback['isteamstack']>0),1,0)
            team_stack_comeback = team_stack_comeback['comeback']
            

            
            team_stack_salaries = teamstackgroup.apply(
                    lambda x: x['salary'].sum()/len(x) if len(x)>1
                    else 0) 
            
            team_stack_ou = teamstackgroup.apply(
                    lambda x: x['o/u'].sum()/len(x) if len(x)>1
                    else 0)

            '''New'''
            team_stack_fpo = teamstackgroup.apply(
                    lambda x: x['month_fpo'].sum()/len(x) if len(x)>1
                    else 0)

            teamstackdf = pd.DataFrame(team_stack_strings).join(
                    pd.DataFrame(team_stack_salaries), rsuffix='_salary').join \
                    (pd.DataFrame(team_stack_ou))
            teamstackdf = teamstackdf.join(pd.DataFrame(team_stack_game, columns=['stack_game']))
            teamstackdf = teamstackdf.join(pd.DataFrame(team_stack_comeback, columns=['comeback']))

            '''New'''
            teamstackdf = teamstackdf.join(pd.DataFrame(team_stack_fpo, columns=['stack_fpo'])).reset_index()

            teamstackdf['0'] = teamstackdf['0'].apply(lambda x: ''.join(
                    sorted(x)) if len(x)>1 else 0)

            teamstackdf = teamstackdf.sort_values(['lineup','0'])
                    
                    
            #part 2 (out agged stats into lists sorted by stack string)
            team_stack_strings2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0].sort_values(['0'])['0'] \
                                     .tolist())

            team_stack_games2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0].sort_values(['0'])['stack_game'] \
                                     .tolist())
            team_stack_games2 = team_stack_games2.apply(lambda x: len(x)==len(set(x)))
        
            team_stack_comeback2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0]['comeback'].sum())
            
            
            team_stack_salaries2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0]['0_salary'] \
                                     .tolist())
            
            team_stack_ou2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0][0] \
                                     .tolist())
            '''New'''
            team_stack_fpo2 = teamstackdf.groupby('lineup').apply(
                    lambda x: x[x[0]!=0]['stack_fpo'].sum()/len(x[x[0]!=0]))
            
            #part 3 create feature column by stack string
            team_stack1 = team_stack_strings2.apply(lambda x: x[0] 
                                                    if len(x)>=1 else 'none')
            team_stack2 = team_stack_strings2.apply(lambda x: x[1]
                                                    if len(x)>=2 else 'none')
            team_stack3 = team_stack_strings2.apply(lambda x: x[2] 
                                                    if len(x)>=3 else 'none')
            team_stack4 = team_stack_strings2.apply(lambda x: x[3] 
                                                    if len(x)==4 else 'none')
            
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

            head_to_head_team_stacks = pd.DataFrame(team_stack_games2.copy(), columns=['head_to_head_team_stacks'])
            head_to_head_team_stacks['head_to_head_team_stacks'] = np.where(head_to_head_team_stacks['head_to_head_team_stacks']==False,1,0)
            head_to_head_team_stacks = head_to_head_team_stacks['head_to_head_team_stacks'] 
            
            #flex analysis
            whose_in_flex = lineups.apply(lambda x: x['Position'].value_counts() \
                                          .subtract(
            pd.Series([1,2,3,1,1], index=['QB','RB','WR','D','TE'])).sort_values() \
                                            .index[-1])
                                          
            #%thrown to positions   
            throw_2rb = lineups['%rb'].sum()
            throw_2wr = lineups['%wr'].sum()
            throw_2te = lineups['%te'].sum()  

            #rolling month fantasy points per snap / fantasy points per opporunity 
            points_per_opp = lineups['month_fpo'].sum()
            points_per_snap = lineups['month_fps'].sum()
            opps_per_snap = points_per_snap/points_per_opp        
            
            analysis = pd.concat([
                                  team_sums,
                                  team_prods,
                                  rbown,
                                  wrown,
                                  teown,
                                  qbown,
                                  down,
                                  sal_std,
                                  plyrs_eq_0,
                                  plyrs_0,
                                  plyrs_less_5,
                                  plyrs_less_10,
                                  plyrs_less_25,
                                  plyrs_abv_90,
                                  plyrs_abv_99,
                                  plyrs_eq_1, 
                                  rbslot1,
                                  rbslot2,
                                  rbslot3, #],axis=1)
                                  wrslot1,
                                  wrslot2,
                                  wrslot3,
                                  wrslot4,
                                  teslot1,
                                  teslot2,
                                  qbslot1,
                                  dslot1,
                                  maxplayersfrom1team,
                                  num_games_represented,
                                  is_playing_d,
                                  chalk_players,
                                  numberofgamestacks,
                                  game_stack1,
                                  game_stack2,
                                  game_stack3,
                                  game_stack4,
                                  game_stack1salary,
                                  game_stack2salary,
                                  game_stack3salary, 
                                  game_stack4salary,
                                  game_stack1ou,
                                  game_stack2ou,
                                  game_stack3ou,
                                  game_stack4ou,
                                  numberofteamstacks,
                                  team_stack1,
                                  team_stack2,
                                  team_stack3,
                                  team_stack4,
                                  team_stack1salary,
                                  team_stack2salary,
                                  team_stack3salary, 
                                  team_stack4salary,
                                  team_stack1ou,
                                  team_stack2ou,
                                  team_stack3ou,
                                  team_stack4ou,
                                  team_stack_fpo2,
                                  head_to_head_team_stacks,
                                  team_stack_comeback2,
                                  whose_in_flex,
                                  throw_2rb,
                                  throw_2wr,
                                  throw_2te,
                                  points_per_opp,
                                  points_per_snap,
                                  opps_per_snap
                                  
                                ], axis=1)
             
            analysis.columns = [
                    'team_actual',
                    'team_proj',
                    'team_proj_own',
                    'team_proj+-',
                    'team_pts',
                    'team_ou',
                    'team_opp+-',
                    'team_snaps',
                    'team_spread',
                    'pass_succ',
                    'rush_succ',
                    'takeaway%',
                    'team_proj_own_prod',
                    'team_rbown',
                    'team_wrown',
                    'team_teown',
                    'team_qbown',
                    'team_down',
                    'salary_std',
                    'plyrs_eq_0',
                    'plyrs_<_0',
                    'plyrs_less_5',
                    'plyrs_less_10',
                    'plyrs_less_25',
                    'plyrs_abv_90',
                    'plyrs_abv_99',
                    'plyrs_eq_1',
                    'rb1_salary',
                    'rb1_snaps',
                    'rb1_opp+-',
                    'rb1_pts',
                    'rb1_proj',
                    'rb1_proj+-',
                    'rb1_ceil',
                    'rb1_spread',
                    'rb1_own',
                    'rb1_bargain',
                    'rb1_leverage',
                    'rb1_optpts',
                    'rb1_rz_succ%',
                    'rb1_rz_td_pct',
                    'rb2_salary',
                    'rb2_snaps',
                    'rb2_opp+-',
                    'rb2_pts',
                    'rb2_proj',
                    'rb2_proj+-',
                    'rb2_ceil',
                    'rb2_spread',
                    'rb2_own',
                    'rb2_bargain',
                    'rb2_leverage',
                    'rb2_optpts',
                    'rb2_rz_succ%',
                    'rb2_rz_td_pct',
                    'rb3_salary',
                    'rb3_snaps',
                    'rb3_opp+-',
                    'rb3_pts',
                    'rb3_proj',
                    'rb3_proj+-',
                    'rb3_ceil',
                    'rb3_spread',
                    'rb3_own',
                    'rb3_bargain',
                    'rb3_leverage',
                    'rb3_optpts',
                    'rb3_rz_succ%',
                    'rb3_rz_td_pct',
                    'wr1_salary',
                    'wr1_snaps',
                    'wr1_opp+-',
                    'wr1_pts',
                    'wr1_proj',
                    'wr1_proj+-',
                    'wr1_ceil',
                    'wr1_spread',
                    'wr1_own',
                    'wr1_bargain',
                    'wr1_leverage',
                    'wr1_optpts',
                    'wr1_rz_td_pct',
                    'wr1_rec_yds%',
                    'wr1_rec_trgts%',
                    'wr1_rec_td%',
                    'wr2_salary',
                    'wr2_snaps',
                    'wr2_opp+-',
                    'wr2_pts',
                    'wr2_proj',
                    'wr2_proj+-',
                    'wr2_ceil',
                    'wr2_spread',
                    'wr2_own',
                    'wr2_bargain',
                    'wr2_leverage',
                    'wr2_optpts',
                    'wr2_rz_td_pct',
                    'wr2_rec_yds%',
                    'wr2_rec_trgts%',
                    'wr2_rec_td%',
                    'wr3_salary',
                    'wr3_snaps',
                    'wr3_opp+-',
                    'wr3_pts',
                    'wr3_proj',
                    'wr3_proj+-',
                    'wr3_ceil',
                    'wr3_spread',
                    'wr3_own',
                    'wr3_bargain',
                    'wr3_leverage',
                    'wr3_optpts',
                    'wr3_rz_td_pct',
                    'wr3_rec_yds%',
                    'wr3_rec_trgts%',
                    'wr3_rec_td%',
                    'wr4_salary',
                    'wr4_snaps',
                    'wr4_opp+-',
                    'wr4_pts',
                    'wr4_proj',
                    'wr4_proj+-',
                    'wr4_ceil',
                    'wr4_spread',
                    'wr4_own',
                    'wr4_bargain',
                    'wr4_leverage',
                    'wr4_optpts',
                    'wr4_rz_td_pct',
                    'wr4_rec_yds%',
                    'wr4_rec_trgts%',
                    'wr4_rec_td%',
                    'te1_salary',
                    'te1_snaps',
                    'te1_opp+-',
                    'te1_pts',
                    'te1_proj',
                    'te1_proj+-',
                    'te1_ceil',
                    'te1_spread',
                    'te1_own',
                    'te1_bargain',
                    'te1_leverage',
                    'te1_optpts',
                    'te1_rz_td_pct',
                    'te1_rec_yds%',
                    'te1_rec_trgts%',
                    'te1_rec_td%',
                    'te2_salary',
                    'te2_snaps',
                    'te2_opp+-',
                    'te2_pts',
                    'te2_proj',
                    'te2_proj+-',
                    'te2_ceil',
                    'te2_spread',
                    'te2_own',
                    'te2_bargain',
                    'te2_leverage',
                    'te2_optpts',
                    'te2_rz_td_pct',
                    'te2_rec_yds%',
                    'te2_rec_trgts%',
                    'te2_rec_td%',
                    'qb1_salary',
                    'qb1_snaps',
                    'qb1_opp+-',
                    'qb1_pts',
                    'qb1_proj',
                    'qb1_proj+-',
                    'qb1_ceil',
                    'qb1_spread',
                    'qb1_own',
                    'qb1_bargain',
                    'qb1_leverage',
                    'qb1_optpts',
                    'd1_salary',
                    'd1_snaps',
                    'd1_opp+-',
                    'd1_pts',
                    'd1_proj',
                    'd1_proj+-',
                    'd1_ceil',
                    'd1_spread',
                    'd1_own',
                    'd1_bargain',
                    'd1_leverage',
                    'd1_optpts',
                    'proj_sacks',
                    'int%',
                    'maxplayersfrom1team',
                    'num_games_represented',
                    'is_playing_d',
                    'chalk_players',
                    'numberofgamestacks',
                    'game_stack1',
                    'game_stack2',
                    'game_stack3',
                    'game_stack4',
                    'game_stack1salary',
                    'game_stack2salary',
                    'game_stack3salary', 
                    'game_stack4salary',
                    'game_stack1ou',
                    'game_stack2ou',
                    'game_stack3ou',
                    'game_stack4ou',
                    'numberofteamstacks',
                    'team_stack1',
                    'team_stack2',
                    'team_stack3',
                    'team_stack4',
                    'team_stack1salary',
                    'team_stack2salary',
                    'team_stack3salary', 
                    'team_stack4salary',
                    'team_stack1ou',
                    'team_stack2ou',
                    'team_stack3ou',
                    'team_stack4ou',
                    'team_stack_fpo2',
                    'head_to_head_stacks',
                    'comeback',
                    'whose_in_flex',
                    'throw_2rb',
                    'throw_2wr',
                    'throw_2te',
                    'points_per_opp',
                    'points_per_snap',
                    'opps_per_snap'
                    ]
            
            analysis = analysis.reset_index()
            analysis['week'] = onlyf
            analysis['id'] = analysis['week'].astype(str) + \
            analysis['lineup'].astype(str) 

            analysis['ismilly'] = np.where(analysis['team_actual']>(historical_winning_scores[str(onlyf)]*.99), 1,0)

            analysis.to_csv('C:\\Users\\{0}\\.fantasy-ryland\\optimized_ml_by_week\\{1}.csv.gz'.format(user, onlyf),
                               compression='gzip', index=False)
        except Exception as e:
            print('Caught exception in worker thread (x = {0}):'.format(onlyf))
        
            # This prints the type, value, and stack trace of the
            # current exception being handled.
            traceback.print_exc()
        
            print()
            raise e
        
        print("--- %s seconds ---" % (time.time() - start_time))

    return True
    

                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
