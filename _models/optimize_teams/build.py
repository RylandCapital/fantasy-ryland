import optimizer

from multiprocessing import Pool


'''Optimize Test Set'''
#optimize teams using optimizer. this creates teams from the 
#fantasylabs scrape script. If you want to add an old week to the 
#dataset you have to use scraper on fantasy labs 
weeks = [
          [1,2],[3,4],[5,6],[7,8],[9,10],[11,12],
          [13,14],[15,16],[120,220],[320,420],[520,620],[720,820],
          [920,1020],[1120,1220],[1320,1420],[1520]
        ]
weeks = [[1420, 1520]]

pool = Pool(processes=len(weeks))
pool.map(optimizer.fantasyze, weeks)
pool.close()

################################################

