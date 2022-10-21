from hmac import trans_36
import time
import os
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from fd_mainline._fantasyml import neuterPredictions

from fd_mainline.config import gameday_week

from dotenv import load_dotenv





load_dotenv()
#fantasy labs username
FLUSER = os.getenv("FLUSER")
#fantasy labs password
FLPASS = os.getenv("FLPASS")

def load_window_fanduel():

    fire = webdriver.FirefoxProfile()
    fire.set_preference("http.response.timeout", 5)
    fire.set_preference("dom.max_script_run_time", 5)
    driver = webdriver.Firefox(firefox_profile=fire)
    webpage = r"https://www.fantasylabs.com/articles/"
    driver.get(webpage)
    time.sleep(2)
    driver.find_element('xpath','/html/body/div[1]/nav/div/div[3]/div[2]/a[2]').click()
    time.sleep(2)
    driver.find_element('xpath', '/html/body/div[3]/form[1]/div[2]/div/input').send_keys(FLUSER)
    time.sleep(2)
    driver.find_element('xpath', '/html/body/div[3]/form[1]/div[3]/div/input').send_keys(FLPASS)
    time.sleep(2)
    driver.find_element('xpath', '/html/body/div[3]/form[1]/div[4]/button').click()
    time.sleep(2)
    driver.find_element('xpath', '//*[@id="menu-item-14874"]').click()
    time.sleep(2)
    driver.find_element('xpath', '/html/body/div[1]/nav/div/div[3]/div[1]/ul/li[2]/ul/li[2]/a').click()
    time.sleep(2)
    driver.set_window_size(3000, 2000)
    time.sleep(2)
    driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[5]/div[1]/a[1]').click()
    driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[5]/div[2]/div[4]').click()
    driver.set_context("chrome")
    win = driver.find_element('tag name', "html")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    driver.set_context("content")

    return driver


def fanduel_ticket(entries=300, max_exposure=150, removals=[], neuter=False):

  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
  path2 = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live\\'.format(user)

  onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
  onlyfiles = [f for f in onlyfiles if f.split('_')[0] == gameday_week]
  teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

  preds = pd.read_csv(path + 'predictions.csv')
  preds=preds.sort_values(by='lineup',ascending=False).drop_duplicates('proba_1',keep='first')

  if neuter==True:
    nps = neuterPredictions(1)[['lineup','proba_1_neutralized']].set_index('lineup')
    preds = preds.set_index('lineup').join(nps)
    preds.reset_index(inplace=True)
    preds['proba_1'] = preds['proba_1_neutralized']
    preds.drop(['proba_1_neutralized'], axis=1, inplace=True)

  picks = preds[['lineup', 'whose_in_flex', 'proba_1', 
   'game_stack4', 'team_stack1', 'team_stack2', 'team_stack3', 'team_stack4',
   'numberofgamestacks', 'numberofteamstacks','num_games_represented']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
  picks.sort_values(by='proba_1', ascending=False, inplace=True)

  ticket = picks.iloc[:(entries*100*9)]
  all_stacks = ticket['team_stack1'].unique().tolist() + \
     ticket['team_stack2'].unique().tolist() + \
      ticket['team_stack3'].unique().tolist() + \
        ticket['team_stack4'].unique().tolist()

  selections = []
  exposures = dict(zip(ticket['name'].unique().tolist(),'0'*len(ticket['name'].unique().tolist())))
  stacks = dict(zip(all_stacks, '0'*len(all_stacks)))

  count = 0
  for i,n in zip(ticket.index.unique(), np.arange(len(ticket.index.unique()))):
      ticket_cols = ['QB','RB','RB','WR','WR','WR','TE','FLEX','DEF']
      df = ticket.loc[i][['pos','Id','whose_in_flex','name','proba_1',
        'team_stack1', 'team_stack2', 'team_stack3', 'team_stack4',
         'numberofgamestacks', 'numberofteamstacks','num_games_represented']].sort_values('Id')
      id2 = sorted(df['Id'].values)
      id2_names = sorted(df['name'].values)
      id2_stacks = pd.concat([df['team_stack1'], df['team_stack2'], df['team_stack3'], df['team_stack4']]).unique()
      maxex = max([float(exposures[i])+1 for i in id2_names])
      removal = len(list(set(id2).intersection(set(removals))))
      proj = df['proba_1'].iloc[0]
      flex = df['whose_in_flex'].iloc[0]
      numberteamstacks = df['numberofteamstacks'].iloc[0]
      numbergamestacks = df['numberofgamestacks'].iloc[0]
      games_represented = df['num_games_represented'].iloc[0]
      df = df[['pos','Id']].sort_values('pos')
      df.set_index('pos', inplace=True)
      df.index = np.where(df.index=='D', 'DEF', df.index)
      flex_pull = df[df.index==flex].iloc[0,0]
      df.index = np.where(df['Id']==flex_pull, 'FLEX', df.index)
      df = df.loc[ticket_cols].drop_duplicates('Id').T
      df['id2'] = str(id2)
      df['name'] = str(id2_names)
      df['proba_1'] = proj
      df['removals'] = removal
      df['numberteamstacks'] = numberteamstacks
      df['numbergamestacks'] = numbergamestacks
      df['games_represented '] = games_represented 
      if maxex<=max_exposure:
        update = [exposures.update({i:float(exposures[i])+1}) for i in id2_names]
        update_stacks = [stacks.update({i:float(stacks[i])+1}) for i in id2_stacks]
        print('Loop:{2} - Count:{1} - Proba_1:{0}'.format(proj,count,n))
        selections.append(df)
        count+=1
        if count==entries:
          break

  upload = pd.concat(selections)
  upload = upload.sort_values(by='proba_1', ascending=False).drop_duplicates('id2',keep='first')
  upload.drop('id2', axis=1).iloc[:entries,:].to_csv(path+'ticket.csv')

  return upload, pd.DataFrame.from_dict(exposures,orient='index').astype(float).sort_values(by=0, ascending=False), pd.DataFrame.from_dict(stacks,orient='index').astype(float).sort_values(by=0, ascending=False)



def easy_remove(ids = []):

  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
  tkt = pd.read_csv(path+'ticket.csv')

  keepers = []
  for i in tkt.index.unique():
    s = tkt.loc[i]
    tf = len(s.isin(ids)[s.isin(ids) == True])
    if tf == 0:
      keepers.append(tkt.loc[i])

  final = pd.concat(keepers, axis=1).T
  final.to_csv(path+'ticket_easy_remove.csv', index=False)





