import os
import pandas as pd


from fd_gpd.config import historical_winning_scores
from fd_gpd._predict.player_stats.helpers import salary_arb


class Data:

  ''''''

  def __init__(self, slate_date, modelname='ensemble'): #string data i.e. '3.9.23', #string model name (deprecate model name)
    try:
      self.slate_date = slate_date
      self.historical_id = historical_winning_scores[slate_date]['slate_id']
      self.weekday = historical_winning_scores[slate_date]['day']
      self.winning_score = historical_winning_scores[slate_date]['winning_score']
      self.optimal = historical_winning_scores[slate_date]['optimal']
      self.modelname = modelname
      self.user = os.getlogin()
    except:
      [print('{0}'.format(i)) for i in historical_winning_scores.keys()]
      print('\n\n ERROR: no data available for this slate :( , choose a data from above :) \n\n')
      
  #returns predictions of gameday pool, if available
  def prediction_probas(self):
    try:
      user = self.user
      path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
      predictions = pd.read_csv(
        path+'_predict\\gpd\\ml_predictions\\{0}\\dataiku_download_{1}.csv'.format(self.slate_date, self.modelname)
        )
      predictions.rename(columns={'proba_1.0':'proba_1'}, inplace=True)
      predictions = predictions.sort_values(by='proba_1', ascending=False)
      predictions = predictions.sort_values(by='lineup',ascending=False) 
    except:
      print('\n\n ERROR: Predictions not available for this slate :( \n\n')

    return predictions
  
  #returns pool of teams generated on gameday that are predicted by algorithm, if available
  def gameday_team_pool(self):
    try:
      path ='C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\optmized_team_pools\\{1}\\'.format(
        self.user,
        self.slate_date
        )
      onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
      teams = pd.concat(
        [pd.read_csv(path + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles]
        )
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
  
  def fantasylabs_historical_stats(self):
    path = os.getcwd() + r"\fd_gpd\_historical\player_stats\by_week"
    try:
      stats = pd.read_csv(path + "\\" + '{0}.csv'.format(self.historical_id)) 
      stats = stats.set_index('RylandID_master')
    except:
      print('\n\n ERROR \n\n')

    return stats
  
  def master(self):
    try:
      user = os.getlogin()
      path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
      path2 ='C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\optmized_team_pools\\{1}\\'.format(
        user,
        self.slate_date
        )

      predictions = pd.read_csv(
        path+'_predict\\gpd\\ml_predictions\\{0}\\dataiku_download_{1}.csv'.format(self.slate_date,self.modelname)
        )
      predictions.rename(columns={'proba_1.0':'proba_1'}, inplace=True)
      predictions = predictions.sort_values(by='proba_1', ascending=False)
      predictions = predictions.sort_values(by='lineup',ascending=False) 
      

      onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
      teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values(
        'lineup',
        ascending=False) for f in onlyfiles]
        )

      #this brings in live stats from last pull(no actual)
      stats = salary_arb(slate_date=self.slate_date)
      stats = stats.set_index('RylandID_master')

      teams = teams[teams['lineup'].isin(predictions['lineup'].unique())]
      #below should be the first time you see teams get smaller because of stats being pulled AFTER teams are made on gameday
      teams = teams.set_index('name').join(stats, how='inner', lsuffix='_ot')
      #below could make teams get smaller because of this changes on fantasylabs from gameday to post gameday
      teams = teams.join(Data(self.slate_date).fantasylabs_historical_stats()[['proj_actpts']], how='inner').reset_index()

      #becuase we had teams lose players above, we must remove any teams that arent full
      nine_confirm = teams.groupby('lineup').apply(lambda x: len(x))
      teams = teams.set_index('lineup').loc[nine_confirm[nine_confirm==9].index.tolist()].reset_index()

      picks = predictions[['lineup', 'proba_1']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
      picks['proba_rank'] = picks['proba_1'].rank(method='max', ascending=False)/9
      picks['check4max'] = picks.groupby(level=0)['team_team'].value_counts().max(level=0)
      picks = picks[picks['check4max']<4]
      picks.sort_values(by='proba_1', ascending=False, inplace=True)

    except:
      print(
        '\n\n ERROR: Some files may be missing to produce master, most likely has historical but no prediction files :( \n\n'
        )

    return picks



class Slate(Data):

  ''''''

  def __init__(self,
                slate_date,
                modelname='ensemble'):
        super().__init__(slate_date, modelname)

  def __repr__(self):
    s = "\nslate: %s" % self.slate_date
    s += "\n\nweekday: %s" % self.weekday
    s += "\nwinning score: %s" % self.winning_score
    s += "\noptimal: %s" % self.optimal
    print(s)
    return ''

  def info(self):
    pass
  
  def report(self):

    rpt = pd.DataFrame([], columns = [
      'Num Teams Predicted',
      'Num Milly Winner in Pool',
      'Highest Proba Milly Winner',
      'Highest Proba Milly Winner Rank',
      'Top Score',
      'Proba of Top Score',
      'Proba Rank', 
      'Would Have Won?'
      ])
    data = Data(slate_date=self.slate_date).master()
    teams = data.groupby(level=0)
  
    top_score_id = teams['proj_actpts'].sum().sort_values().index[-1]
    top_proba_id = teams['proba_1'].first().sort_values().index[-1]
    top_ticket_ids = teams['proba_1'].first().sort_values().index[-150:]
    milly_winner_ids = teams['proj_actpts'].sum()[teams['proj_actpts'].sum()>self.winning_score].index

    rpt.loc['', 'Num Teams Predicted'] = len(teams)
    rpt.loc['', 'Num Milly Winner in Pool'] = '{0} ({1}%)'.format(len(teams['proj_actpts'].sum()[teams['proj_actpts'].sum()>self.winning_score]),
                                                                  round(100*(len(teams['proj_actpts'].sum()[teams['proj_actpts'].sum()>self.winning_score])/len(teams)),2))
    rpt.loc['','Highest Proba Milly Winner'] = round(data.loc[milly_winner_ids]['proba_1'].max(),4)
    rpt.loc['','Highest Proba Milly Winner Rank'] = round(data.loc[milly_winner_ids]['proba_rank'].min(),4)

    rpt.loc['Top Team Pool', 'Top Score'] = teams['proj_actpts'].sum().loc[top_score_id]
    rpt.loc['Top Team Pool', 'Proba of Top Score'] = teams['proba_1'].first().loc[top_score_id]
    rpt.loc['Top Team Pool', 'Proba Rank'] = teams['proba_rank'].first().loc[top_score_id]
    rpt.loc['Top Team Pool', 'Would Have Won?'] = teams['proj_actpts'].sum().loc[top_score_id]>self.winning_score
    
    rpt.loc['Top Proba', 'Top Score'] = teams['proj_actpts'].sum().loc[top_proba_id]
    rpt.loc['Top Proba', 'Proba of Top Score'] = teams['proba_1'].first().loc[top_proba_id]
    rpt.loc['Top Proba', 'Proba Rank'] = teams['proba_rank'].first().loc[top_proba_id]
    rpt.loc['Top Proba', 'Would Have Won?'] = teams['proj_actpts'].sum().loc[top_proba_id]>self.winning_score

    rpt.loc['Top Ticket', 'Top Score'] = teams['proj_actpts'].sum().loc[top_ticket_ids].max()
    rpt.loc['Top Ticket', 'Would Have Won?'] = teams['proj_actpts'].sum().loc[top_ticket_ids].max()>self.winning_score
    

    rpt.to_csv(r'C:\Users\rmathews\Downloads\report_{0}.csv'.format(self.slate_date))


    return data


   


