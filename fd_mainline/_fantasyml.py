import pandas as pd
import numpy as np
from sklearn.model_selection import PredefinedSplit
from sklearn.preprocessing import MinMaxScaler
import scipy
import os
    
    
def _neutralize( df, columns, by, proportion=1.0):
    scores = df[columns]
    exposures = df[by].values
    scores = scores - proportion * exposures.dot(
            np.linalg.pinv(exposures).dot(scores))
    return scores / scores.std(ddof=0)

def _normalize(df):
    X = (df.rank(method="first") - 0.5) / len(df)
    return scipy.stats.norm.ppf(X)

def normalize_and_neutralize(df, columns, by, proportion=1.0):
    # Convert the scores to a normal distribution
    df[columns] = _normalize(df[columns])
    df[columns] = _neutralize(df, columns, by, proportion)
    return df[columns]

def neuterPredictions(proportion, model=''):
    user = os.getlogin()
    path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
    preds = pd.read_csv(path+'predictions_{0}.csv'.format(model))
    removals = ['col_0', 'is_playing_d', 'game_stack1', 'game_stack2', 'game_stack3', 'game_stack4',
      'team_stack1', 'team_stack2', 'team_stack3', 'team_stack4',  'head_to_head_stacks', 'comeback',
      'whose_in_flex', 'team_stack1salary', 'team_stack2salary', 'team_stack3salary', 'team_stack4salary', 'team_stack1ou', 'team_stack2ou',
       'team_stack3ou', 'team_stack4ou',  'game_stack1salary', 'game_stack2salary', 'game_stack3salary', 'game_stack4salary', 'game_stack1ou',
        'game_stack2ou', 'game_stack3ou', 'game_stack4ou','id', 'proba_0', 'prediction', 'lineup', 'week']
    removals = [x for x in preds.columns if x not in removals]
    df = preds[removals]
    features = df.columns.tolist()
    features.remove('proba_1')
    df['era'] = 1
    df['proba_1_neutralized'] =  df.groupby('era').apply(
        lambda x: normalize_and_neutralize(x, ['proba_1'],
                                                features, proportion))
    return preds.join(df['proba_1_neutralized']).sort_values(by='proba_1_neutralized', ascending=False)

   
