import time
import os
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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


def fanduel_ticket(predictions, teams, entries=150, injuries=[]):

  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  

  picks = predictions[['lineup', 'whose_in_flex', 'prediction']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
  picks.sort_values(by='prediction', ascending=False, inplace=True)

  ticket = picks.iloc[:(entries*60)]

  remove = injuries 
  tests = []
  for i in ticket.index.unique():
    ticket_cols = ['QB','RB','RB','WR','WR','WR','TE','FLEX','DEF']
    df = ticket.loc[i][['pos','Id','whose_in_flex','prediction']].sort_values('Id')
    id2 = sorted(df['Id'].values)
    injury = len(list(set(id2).intersection(set(remove))))
    proj = df['prediction'].iloc[0]
    flex = df['whose_in_flex'].iloc[0]
    df = df[['pos','Id']].sort_values('pos')
    df.set_index('pos', inplace=True)
    df.index = np.where(df.index=='D', 'DEF', df.index)
    flex_pull = df[df.index==flex].iloc[0,0]
    df.index = np.where(df['Id']==flex_pull, 'FLEX', df.index)
    df = df.loc[ticket_cols].drop_duplicates('Id').T
    df['id2'] = str(id2)
    df['prediction'] = proj
    df['injury'] = injury
    tests.append(df)
  upload = pd.concat(tests)
  upload = upload[upload['injury']==0].sort_values(by='prediction', ascending=False).drop_duplicates('id2',keep='first')
  upload.iloc[:entries,:-2].to_csv(path+'ticket.csv')

  return upload

