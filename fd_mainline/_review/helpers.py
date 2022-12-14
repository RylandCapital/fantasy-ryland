import pandas as pd
import os 

from fd_mainline._fantasyml import neuterPredictions


def analyze_gameday_pool_with_ids(ids=[], historical_id = 50, week='10.5.22', neuter=False, model=''):

    user = os.getlogin()
    path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
    path2 = 'C:\\Users\\{0}\\.fantasy-ryland\\model_tracking\\teams\\{1}\\'.format(user,week)

    predictions = pd.read_csv(path+'model_tracking\\predictions\\{0}_{1}.csv'.format(week, model))
    predictions = predictions.sort_values(by='lineup',ascending=False) 

    if neuter==True:
        nps = neuterPredictions(1, model, slate_date=week)[['lineup','proba_1_neutralized']].set_index('lineup')
        predictions = predictions.set_index('lineup').join(nps)
        predictions.reset_index(inplace=True)
        predictions['proba_1'] = predictions['proba_1_neutralized']
        predictions.drop(['proba_1_neutralized'], axis=1, inplace=True)

    onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
    onlyfiles = [f for f in onlyfiles if f.split('_')[0] == week]
    teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

    picks = predictions[['lineup', 'whose_in_flex', 'proba_1']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
    picks.sort_values(by='proba_1', ascending=False, inplace=True)

    statspath = os.getcwd() + r"\fd_mainline\_historical\player_stats\by_week"
    stats = pd.read_csv(statspath + "\\" + '{0}.csv'.format(historical_id)) 
    stats.set_index('RylandID_master', inplace=True)

    df = picks.reset_index().set_index('name').join(stats[['act_pts']]).reset_index()
    df['proba_%'] = df['proba_1'].rank(method='max',pct=True)
    df['proba_rank'] = df['proba_1'].rank(method='max', ascending=False)/9
    dflineup = df.groupby(['lineup'])
    df.index = df['lineup']
    team_scores = dflineup['act_pts'].sum().sort_values()
    ticket_scores = dflineup[['act_pts']].sum().join(dflineup['proba_1'].first()).sort_values(by='proba_1', ascending=False).loc[ids]
    act_describe = team_scores.describe().round(2)
    player_pcts =  (df['index'].value_counts()/(df['index'].value_counts().sum()/9)).round(5)

    top = df.loc[team_scores.index[-1]][['index','act_pts','proba_1', 'proba_%', 'proba_rank']] 
    corr = pd.concat([dflineup[['act_pts']].sum(), (dflineup[['proba_1']].first())], axis=1)
    corr['pct_proba'] = corr['proba_1'].rank(pct=True)
    top['pct_proba'] = corr.loc[top.index[0]].pct_proba
    corr['act_pts'].corr(corr['proba_1'])

    duplicates = len(teams.groupby(['lineup'])) - len(teams.groupby(['lineup'])['name'].sum().apply(lambda x: ''.join(sorted(x))).unique())

    return df, team_scores, act_describe, player_pcts, top, corr, duplicates, ticket_scores
