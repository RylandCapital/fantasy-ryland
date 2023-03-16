import os
import pandas as pd


from fd_gpd.config import historical_winning_scores
from fd_gpd._predict.player_stats.helpers import salary_arb


class Data:

  ''''''

  def __init__(self, slate_date, modelname='ensemble'): #string data i.e. '3.9.23', #string model name (deprecate model name)
    try:
      self.slate_date = slate_date
      self.modelname = modelname
      self.user = os.getlogin()

      #create error if slate is not available and let user know
      historical_winning_scores[slate_date]['day']
    except:
      [print('{0}'.format(i)) for i in historical_winning_scores.keys()]
      print('\n\n ERROR: no data available for this slate :( , choose a data from above :) \n\n')
      
  #returns predictions of gameday pool, if available
  def prediction_probas(self):
    try:
      user = self.user
      path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
      predictions = pd.read_csv(path+'_predict\\gpd\\ml_predictions\\{0}\\dataiku_download_{1}.csv'.format(
        self.slate_date, self.modelname))
      predictions.rename(columns={'proba_1.0':'proba_1'}, inplace=True)
      predictions = predictions.sort_values(by='proba_1', ascending=False)
      predictions = predictions.sort_values(by='lineup',ascending=False) 
    except:
      print('\n\n ERROR: Predictions not available for this slate :( \n\n')

    return predictions
  
  #returns pool of teams generated on gameday that are predicted by algorithm, if available
  def gameday_team_pool(self):
    try:
      path ='C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\optmized_team_pools\\{1}\\'.format(self.user,self.slate_date)
      onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
      teams = pd.concat([pd.read_csv(path + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])
    except:
      print('\n\n ERROR: Gameday team pool not available for this slate :( \n\n')
    
    return teams
  
  #return fantasy labs file that was pulled on gameday WITH DraftKings salaries as well, if available
  def fantasylabs_live_stats(self):
    try:
      stats = salary_arb(slate_date=self.slate_date)
      stats = stats.set_index('RylandID_master')
    except:
      print('\n\n ERROR: Gameday FantasyLabs file not available for this slate :( \n\n')

    return stats





class Report:

  ''''''

  def __init__(self, slate_date):
    pass


class Slate:

  ''''''

  def __init__(self, slate_date):
    try:
      self.slate = slate_date
      self.weekday = historical_winning_scores[slate_date]['day']
      self.winning_score = historical_winning_scores[slate_date]['winning_score']
      self.optimal = historical_winning_scores[slate_date]['optimal']
    except:
      print('\n\n ERROR: slate not available, try another date \n\n')

  def __repr__(self):
    s = "\nslate: %s" % self.slate
    s += "\n\nweekday: %s" % self.weekday
    s += "\nwinning score: %s" % self.winning_score
    s += "\noptimal: %s" % self.optimal
    return print(s)
    

  def prediction_report(self):
    pass





def inspect_preds(model='ensemble', slate_date=''):

  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
  path2 ='C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\optmized_team_pools\\{1}\\'.format(user,slate_date)
  path3 = os.getcwd() + r"\fd_gpd\_predict\player_stats\by_week"

  predictions = pd.read_csv(path+'_predict\\gpd\\ml_predictions\\{0}\\dataiku_download_{1}.csv'.format(slate_date, model))
  predictions.rename(columns={'proba_1.0':'proba_1'}, inplace=True)
  predictions = predictions.sort_values(by='proba_1', ascending=False)
  predictions = predictions.sort_values(by='lineup',ascending=False) 
  

  onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
  teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

  stats = salary_arb(slate_date=slate_date)
  stats = stats.set_index('RylandID_master')

  teams = teams[teams['lineup'].isin(predictions['lineup'].unique())]
  #teams may be reduced based on players being added/removed on fantasy labs 
  #from the time players are first pulled and repulled at gametime
  teams = teams.set_index('name').join(stats, how='inner', lsuffix='_ot').reset_index()

  
  nine_confirm = teams.groupby('lineup').apply(lambda x: len(x))
  teams = teams.set_index('lineup').loc[nine_confirm[nine_confirm==9].index.tolist()].reset_index()

  return teams
  
   


