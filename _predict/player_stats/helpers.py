import time
import os
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv

from config import gameday_week

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
    driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[3]/nav/ul/li[2]/a').click()
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


def fanduel_ticket(entries=300, max_exposure=300, injuries=[]):

  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
  path2 = 'C:\\Users\\{0}\\.fantasy-ryland\\optimized_teams_by_week_live\\'.format(user)

  onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
  onlyfiles = [f for f in onlyfiles if f.split('_')[0] == gameday_week]
  teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

  preds = pd.read_csv(path + 'predictions.csv')
  preds=preds.sort_values(by='lineup',ascending=False).drop_duplicates('proba_1',keep='first')

  picks = preds[['lineup', 'whose_in_flex', 'proba_1']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
  picks.sort_values(by='proba_1', ascending=False, inplace=True)

  ticket = picks.iloc[:(entries*100*9)]

  selections = []
  exposures = dict(zip(ticket['name'].unique().tolist(), '0'*len(ticket['name'].unique().tolist())))
  count = 0
  for i,n in zip(ticket.index.unique(), np.arange(len(ticket.index.unique()))):
      ticket_cols = ['QB','RB','RB','WR','WR','WR','TE','FLEX','DEF']
      df = ticket.loc[i][['pos','Id','whose_in_flex','name','proba_1']].sort_values('Id')
      id2 = sorted(df['Id'].values)
      id2_names = sorted(df['name'].values)
      maxex = max([float(exposures[i])+1 for i in id2_names])
      injury = len(list(set(id2).intersection(set(injuries))))
      proj = df['proba_1'].iloc[0]
      flex = df['whose_in_flex'].iloc[0]
      df = df[['pos','Id']].sort_values('pos')
      df.set_index('pos', inplace=True)
      df.index = np.where(df.index=='D', 'DEF', df.index)
      flex_pull = df[df.index==flex].iloc[0,0]
      df.index = np.where(df['Id']==flex_pull, 'FLEX', df.index)
      df = df.loc[ticket_cols].drop_duplicates('Id').T
      df['id2'] = str(id2)
      df['name'] = str(id2_names)
      df['proba_1'] = proj
      df['injury'] = injury

      if maxex<=max_exposure:
        update = [exposures.update({i:float(exposures[i])+1}) for i in id2_names]
        print('Loop:{2} - Count:{1} - Proba_1:{0}'.format(proj,count,n))
        selections.append(df)
        count+=1
        if count==entries:
          break

  upload = pd.concat(selections)
  upload = upload.sort_values(by='proba_1', ascending=False).drop_duplicates('id2',keep='first')
  upload.drop('id2', axis=1).iloc[:entries,:].to_csv(path+'ticket.csv')

  return upload, pd.DataFrame.from_dict(exposures,orient='index').astype(float).sort_values(by=0, ascending=False)

