import os

from _historical.optimize.optimize import fantasyze
from multiprocessing import Pool

from config import curr_optimize_weeks



'''Create Local Export Env'''
user = os.getlogin()
# Specify path
path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path)
  os.mkdir(path+'optimized_teams_by_week\\')



'''Optimize New Histoical Teams'''
#optimize teams using optimizer. this creates teams from the 
#fantasylabs scrape script. If you want to add an old week to the 
#dataset you have to use scraper on fantasy labs 
weeks = curr_optimize_weeks

pool = Pool(processes=len(weeks))
pool.map(fantasyze, weeks)
pool.close()

################################################

