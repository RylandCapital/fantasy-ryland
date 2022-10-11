import pandas as pd
import os 



def analyze_gameday_pool(historical_id = 49, week='9.28.22'):

    user = os.getlogin()
    path = 'C:\\Users\\{0}\\.fantasy-ryland\\_predictions_vault\\{1}\\'.format(user, week)
    path2 = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live\\'.format(user)

    predictions = pd.read_csv(path+'predictions.csv')

    onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
    onlyfiles = [f for f in onlyfiles if f.split('_')[0] == week]
    teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

    picks = predictions[['lineup', 'whose_in_flex', 'proba_1']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
    picks.sort_values(by='proba_1', ascending=False, inplace=True)

    statspath = os.getcwd() + r"\_historical\player_stats\by_week"
    stats = pd.read_csv(statspath + "\\" + '{0}.csv'.format(historical_id)) 
    stats.set_index('RylandID_master', inplace=True)

    df = picks.reset_index().set_index('RylandID').join(stats[['act_pts']]) #df = teams.reset_index().set_index('RylandID').join(stats[['act_pts']])
    dflineup = df.groupby(['lineup'])
    df.index = df['lineup']
    team_scores = dflineup['act_pts'].sum().sort_values()
    act_describe = team_scores.describe().round(2)
    player_pcts =  (df['Unnamed: 0.1'].value_counts()/(df['Unnamed: 0.1'].value_counts().sum()/9)).round(5)

    top = df.loc[team_scores.index[-1]][['Unnamed: 0.1','act_pts','proba_1']] 
    corr = pd.concat([dflineup[['act_pts']].sum(), (dflineup[['proba_1']].first())], axis=1)
    corr['pct_proba'] = corr['proba_1'].rank(pct=True)
    top['pct_proba'] = corr.loc[top.index[0]].pct_proba

    duplicates = len(teams.groupby(['lineup'])) - len(teams.groupby(['lineup'])['name'].sum().apply(lambda x: ''.join(sorted(x))).unique())

    return df, team_scores, act_describe, player_pcts, top, corr, duplicates
