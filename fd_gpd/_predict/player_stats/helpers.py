from hmac import trans_36
import time
import os
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv
from fd_gpd._predict.optimize.optimize_proj import fantasyze_proj



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
    driver.find_element('xpath', '//*[@id="menu-item-37607"]').click()
    time.sleep(2)
    driver.find_element('xpath', '/html/body/div[1]/nav/div/div[3]/div[1]/ul/li[7]/ul/li[1]/a').click()
    time.sleep(2)
    driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[5]/div[1]/a[1]').click()
    time.sleep(2)
    driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[5]/div[2]/div[4]').click()
    time.sleep(2)
    driver.set_window_size(3000, 2000)
    driver.set_context("chrome")
    win = driver.find_element('tag name', "html")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    win.send_keys(Keys.CONTROL + "-")
    driver.set_context("content")

    return driver

def fanduel_ticket_optimized(slate_date='1.9.23', ids=[], model='ensemble'):

  user = os.getlogin()
  user = os.getlogin()
  path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)  
  path2 ='C:\\Users\\{0}\\.fantasy-ryland\\_predict\\gpd\\optmized_team_pools\\{1}\\'.format(user,slate_date)
  path3 = os.getcwd() + r"\fd_gpd\_predict\player_stats\by_week"

  preds = pd.read_csv(path+'_predict\\gpd\\ml_predictions\\{0}\\dataiku_download_{1}.csv'.format(slate_date, model))
  preds.rename(columns={'proba_1.0':'proba_1'}, inplace=True)
  preds = preds.sort_values(by='proba_1', ascending=False).iloc[:100000]
  preds = preds.sort_values(by='lineup',ascending=False) 
  

  onlyfiles = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]
  teams = pd.concat([pd.read_csv(path2 + f, compression='gzip').sort_values('lineup',ascending=False) for f in onlyfiles])

  stats = pd.read_csv(path3 + "\\" + '{0}.csv'.format(slate_date)) 
  stats = stats.set_index('RylandID_master')

  teams = teams[teams['lineup'].isin(preds['lineup'].unique())]
  teams = teams.set_index('name').join(stats, how='inner', lsuffix='_ot').reset_index()
  nine_confirm = teams.groupby('lineup').apply(lambda x: len(x))
  teams = teams.set_index('lineup').loc[nine_confirm[nine_confirm==9].index.tolist()].reset_index()

  picks = preds[['lineup', 'proba_1']].set_index('lineup').join(teams.set_index('lineup'), how='inner')
  picks.sort_values(by='proba_1', ascending=False, inplace=True)

  ticket = picks.loc[ids]


  opt_team = fantasyze_proj(slate_date=slate_date)
  opt_team_score = opt_team['actual'].sum()

  selections = []
  exposures = dict(zip(ticket['name'].unique().tolist(),'0'*len(ticket['name'].unique().tolist())))

  for i,n in zip(ticket.index.unique(), np.arange(len(ticket.index.unique()))):
      ticket_cols = ['C','C','W','W','D','D','FLEX','FLEX','G']
      df = ticket.loc[i][['pos','Id','name','proba_1',
        'dkSalary', 'Salary', 'proj_proj']].sort_values('Id')
      id2 = sorted(df['Id'].values)
      id2_names = sorted(df['name'].values)

      proj = df['proba_1'].iloc[0]
      proj_pts = df['proj_proj'].sum()
      dksalary = df['dkSalary'].sum()
      salary = df['Salary'].sum()

      df = df[['pos','Id']].sort_values('pos')
      df.set_index('pos', inplace=True)

      sections = []
      for l in df.index.unique():
        t = pd.DataFrame(df.loc[l])
        if len(t) > 2:
          t.index = [l,l] + ['FLEX']*(len(t)-2)
          sections.append(t)
        elif len(t) == 1:
          sections.append(t.T)
        else:
          sections.append(t)

      df = pd.concat(sections).loc[ticket_cols].drop_duplicates('Id').T
      df['id2'] = str(id2)
      df['name'] = str(id2_names)
      df['proba_1'] = proj
      df['projected'] = proj_pts
      df['pct_optimal'] = round(proj_pts/opt_team_score,2)
      df['Salary'] = salary
      df['dkSalary'] = dksalary

      update = [exposures.update({i:float(exposures[i])+1}) for i in id2_names]
      selections.append(df)

        

  upload = pd.concat(selections)
  #remove duplicate teams (id2)
  upload = upload.sort_values(by='proba_1', ascending=False).drop_duplicates('id2',keep='first')
  #download final ticket ids for backtesting historically 
  upload.drop('id2', axis=1).to_csv(path+'_predict\\gpd\\uploaded_gameday_tickets\\{0}_{1}_ticket.csv'.format(slate_date, model))
  exposuresdf = (pd.DataFrame.from_dict(exposures,orient='index').astype(float).sort_values(by=0, ascending=False)/len(selections)*100).round(1)
  exposuresdf = exposuresdf.join(ticket[['name', 'Team', 'pos', 'Salary', 'proj_proj']].set_index('name')).drop_duplicates().sort_values(by=0, ascending=False)
  exposuresdf.columns = ['my_ownership', 'Team', 'Position', 'Salary', 'Projected Points']
  exposuresdf.to_csv(path+'_predict\\gpd\\uploaded_gameday_tickets\\{0}_{1}_exposures.csv'.format(slate_date, model))


  return upload, exposuresdf


def salary_arb(slate_date):

  '''joins dk and fanduel salaries'''
  
  path = os.getcwd() + r"\fd_gpd\_predict\player_stats\by_week"
  path2 = os.getcwd() + r"\fd_gpd\_predict\player_stats"
  stats = pd.read_csv(path + "\\" + '{0}.csv'.format(slate_date)) 
  stats = stats.set_index('RylandID_master')
  try:
    stats = stats.drop('dkSalary', axis=1)
  except:
    pass

  path3 = os.getcwd() + r"\fd_gpd\_predict\player_stats\dk_files"
  dk = pd.read_csv(path3 + "\\" + '{0}.csv'.format(slate_date)) 
  dk['TeamAbbrev'] = np.where(dk['TeamAbbrev']=='WAS', 'WSH', dk['TeamAbbrev'])
  dk['TeamAbbrev'] = np.where(dk['TeamAbbrev']=='CLS', 'CBJ', dk['TeamAbbrev'])
  dk['combo_id'] = dk['Name'].str.lower().str.replace(' ','')+\
                  dk['TeamAbbrev']
  stats['combo_id'] = stats['Nickname'].str.lower().str.replace(' ','')+\
                       stats['Team']
  
  dk.set_index('combo_id', inplace=True)
  stats.reset_index(inplace=True)
  stats.set_index('combo_id', inplace=True)
  dk = dk[['Salary']].rename(columns={'Salary':'dkSalary'})

  df = stats.join(dk,how='left')
  df.to_csv(path2 + "\\" + 'dkcheck.csv')

  df.set_index('RylandID_master').to_csv(path + "\\" + '{0}.csv'.format(slate_date))

  return df






