import pandas as pd
import time
import numpy as np
import os

from selenium.webdriver.common.keys import Keys

from fd_mainline._predict.player_stats import helpers

from fd_mainline.config import rbcolumns_hist, wrcolumns_hist, tecolumns_hist, qbcolumns_hist, defcolumns_hist, shift, \
    rbcolumns_hist_shift, wrcolumns_hist_shift, tecolumns_hist_shift, qbcolumns_hist_shift, defcolumns_hist_shift


def pull_stats_live(weeks=[], strdates=[]):
    
        driver = helpers.load_window_fanduel()
        time.sleep(10)
  
        for date, we in zip(strdates[0:], weeks):

            try:

                print('\n\n\ncurrently scraping date : {0}'.format(date))

                driver.get('https://www.fantasylabs.com/nfl/player-models/?date={0}'.format(date))
                time.sleep(5)
                
                #%%
                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[2]/a').click()
                time.sleep(5)
                
                name = 'RB'
                
                if shift==False:
                    rbcolumns =  rbcolumns_hist
                else:
                    rbcolumns = rbcolumns_hist_shift
                
                rbcolumns.remove('act_pts')
                #this gets the little blue number that shows number of players in that position that day
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                #loop on for left columns
                #this loop gets the first 4 columns, starting at column 3 as you can see in
                #np.arange(3,7) below
                columns = []
                column_names = ['rating', 'name', 'salary', 'team', 'opp']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 

                                            
                
                #loop 2 for right columns
                #this loop gets all columns, starting at column 1 as you can see in
                #np.arange(1, len(names)) below
                #17,18,19,20 
                rcolumns = []
                rcolumn_names = rbcolumns
                len_names = len(rcolumn_names)
                for n, t in zip(rcolumn_names, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finalrb = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finalrb['pos'] = name
                finalrb['week'] = we
                finalrb.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))
                

                rbdf = finalrb.copy()
                #rbdf = rbdf.drop(['sr2', 'buzz2'], axis=1)
                #%%
                driver.refresh()
                time.sleep(10)
                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[3]/a').click()
                time.sleep(5)
                
                
                name = 'WR'
                
                if shift==False:
                    wrcolumns =  wrcolumns_hist
                else: 
                    wrcolumns = wrcolumns_hist_shift

                wrcolumns.remove('act_pts')                         
                #this gets the little blue number that shows number of players in that position that day
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                #loop on for left columns
                #this loop gets the first 4 columns, starting at column 3 as you can see in
                #np.arange(3,7) below
                columns = []
                column_names = ['rating', 'name', 'salary', 'team', 'opp']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 

                                            
                
                #loop 2 for right columns
                #this loop gets all columns, starting at column 1 as you can see in
                #np.arange(1, len(names)) below
                #
                rcolumns = []
                rcolumn_names = wrcolumns
                len_names = len(rcolumn_names)
                for n, t in zip(rcolumn_names, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finalwr = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finalwr['pos'] = name
                finalwr['week'] = we
                finalwr.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))
            
                    
                wrdf = finalwr.copy()
            
                #%%
                driver.refresh()
                time.sleep(10)
                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[4]/a').click()
                time.sleep(5)

                name = 'TE'
                
                if shift==False:
                    tecolumns =  tecolumns_hist
                else:
                    tecolumns = tecolumns_hist_shift

                tecolumns.remove('act_pts')
                #this gets the little blue number that shows number of players in that position that day
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                #loop on for left columns
                #this loop gets the first 4 columns, starting at column 3 as you can see in
                #np.arange(3,7) below
                columns = []
                column_names = ['rating', 'name', 'salary', 'team', 'opp']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 

                                            
                
                #loop 2 for right columns
                #this loop gets all columns, starting at column 1 as you can see in
                #np.arange(1, len(names)) below
                #
                rcolumns = []
                rcolumn_names = tecolumns
                len_names = len(rcolumn_names)
                for n, t in zip(rcolumn_names, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finalte = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finalte['pos'] = name
                finalte['week'] = we
                finalte.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))

                tedf = finalte.copy()
                
                
                #%%
                driver.refresh()
                time.sleep(10)

                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[1]/a').click()
                time.sleep(5)
                
                name = 'QB'
                
                
                #this gets the little blue number that shows number of players in that position that day
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                #loop on for left columns
                #this loop gets the first 4 columns, starting at column 3 as you can see in
                #np.arange(3,7) below
                columns = []
                column_names = ['rating', 'name', 'salary', 'team', 'opp']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 

                                            
                
                #loop 2 for right columns
                #this loop gets all columns, starting at column 1 as you can see in
                #np.arange(1, len(names)) below
                #
                rcolumns = []
                if shift==False:
                    qbcolumns =  qbcolumns_hist
                else:
                    qbcolumns = qbcolumns_hist_shift

                qbcolumns.remove('act_pts')

                len_names = len(qbcolumns)
                for n, t in zip(qbcolumns, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finalqb = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finalqb['pos'] = name
                finalqb['week'] = we
                finalqb.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))

                qbdf = finalqb.copy()  
            
                #%%
                driver.refresh()
                time.sleep(10)

                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[6]/a').click()
                time.sleep(5)
                    
                name = 'DEF'
            
                
                #this gets the little blue number that shows number of players in that position that day
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                #loop on for left columns
                #this loop gets the first 4 columns, starting at column 3 as you can see in
                #np.arange(3,7) below
                columns = []
                column_names = ['rating', 'name', 'salary', 'team', 'opp']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 

                                            
                #loop 2 for right columns
                #this loop gets all columns, starting at column 1 as you can see in
                #np.arange(1, len(names)) below
                #
                rcolumns = []
                if shift==False:
                    defcolumns =  defcolumns_hist
                else:
                    defcolumns = defcolumns_hist_shift

                defcolumns.remove('act_pts')
                len_names = len(defcolumns)
                for n, t in zip(defcolumns, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finaldef = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finaldef['pos'] = name
                finaldef['week'] = we
                finaldef.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))


                
                defdf = finaldef.copy()   
            
                #%%  
                '''CLEANING'''
                
                master = pd.concat([qbdf, rbdf, wrdf, tedf, defdf], sort=False).reset_index(drop=True)
                master['salary'] = master['salary'].apply(lambda x: int(x[1:]))
                master['snaps'] = master['snaps'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                # master['act_pts'] = master['act_pts'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['proj'] = master['proj'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['ceil'] = master['ceil'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['floor'] = master['floor'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['proj+-'] = master['proj+-'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['pts/sal'] = master['pts/sal'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['proj_own'] = master['proj_own'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna('0').apply(lambda x: float(x))
                master['impld_pts'] = master['impld_pts'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['lev_rank'] = master['lev_rank'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['leverage'] = master['leverage'].apply(lambda x: x.replace('','50%') if len(x)==0 else x).apply(lambda x: x.replace(' ','50%') if len(x)==1 else x).fillna(0).apply(lambda x: float(x[:-1])/100)
                master['sr'] = master['sr'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x[:-1])/100)
                master['buzz'] = master['buzz'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['pro'] = master['pro'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['my'] = master['my'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['bargain'] = master['bargain'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x[:-1])/100)
                master['opp+-'] = master['opp+-'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['pts'] = master['pts'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['opppts'] = master['opppts'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['delta'] = master['delta'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['spread'] = master['spread'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['o/u'] = master['o/u'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['spread%'] = master['spread%'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['comp'] = master['comp'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['att'] = master['att'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['yards'] = master['yards'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['%'] = master['%'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['y/a'] = master['y/a'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['adj ypa'] = master['adj ypa'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).astype(float)
                master['td'] = master['td'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['long'] = master['long'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master["%rb"] = master["%rb"].apply(lambda x: str(x).replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['%wr'] = master['%wr'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['%te'] = master['%te'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['%td'] = master['%td'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['int%'] = master['int%'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)
                master['sack%'] = master['sack%'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)
                master['rush-att'] = master['rush-att'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['not sure'] = master['not sure'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['rush_yards'] = master['rush_yards'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['rush_y/a'] = master['rush_y/a'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['rush_td'] = master['rush_td'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['success'] = master['success'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['rz_opp'] = master['rz_opp'].fillna(0).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).astype(float)
                master['rz_opp10'] = master['rz_opp10'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['rz-opp5'] = master['rz-opp5'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['temp'] = master['temp'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['humidity'] = master['humidity'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['precip%'] = master['precip%'].apply(lambda x: x.replace(' ','0') if len(x)==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['month_ppg'] = master['month_ppg'].apply(lambda x: x.replace('','0') if len(x)==0 else x).fillna(0).apply(lambda x: float(x))
                master['month_change'] = master['month_change'].apply(lambda x: x.replace('','00') if len(str(x))==0 else x).apply(lambda x: int(x[1:]))
                master['month_fpo'] = master['month_fpo'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['month_fps'] = master['month_fps'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['consistency'] = master['consistency'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x[:-1]))
                master['upside'] = master['upside'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x[:-1])/100)
                master['duds'] = master['duds'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x[:-1])/100)
                master['count'] = master['count'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x))
                master['year_ppg'] = master['year_ppg'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x))
                master['year+-'] = master['year+-'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x))
                master['year_change'] = master['year_change'].apply(lambda x: x.replace('$','')).apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).astype(float)
                master['year_fpo'] = master['year_fpo'].apply(lambda x: x.replace(' ','0') if len(str(x))==0 else x).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['year_fps'] = master['year_fps'].apply(lambda x: x.replace(' ','0') if len(str(x))==0 else x).apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).apply(lambda x: float(x))
                master['year_consistency'] = master['year_consistency'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x[:-1]))
                master['year_upside'] = master['year_upside'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x[:-1])/100)
                master['year_duds'] = master['year_duds'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x[:-1])/100)
                master['year_count'] = master['year_count'].apply(lambda x: x.replace('','0') if (len(x)==0) | (len(x)==1) else x).fillna(0).apply(lambda x: float(x))
                master['rush_td%'] = master['rush_td%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['rush_yards%'] = master['rush_yards%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['snaps%'] = master['snaps%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['rush_att'] = master['rush_att'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['rec_trgts'] = master['rec_trgts'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['not_sure2'] = master['not_sure2'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['rec_yards'] = master['rec_yards'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['rec_long'] = master['rec_long'].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0).astype(float)
                master['rec_yr'] = master['rec_yr'].apply(lambda x: x.replace('','0') if (len(str(x))==0) | (len(str(x))==1) else x).fillna(0).apply(lambda x: float(x))
                master['rec_td'] = master['rec_td'].apply(lambda x: x.replace('','0') if (len(str(x))==0) | (len(str(x))==1) else x).fillna(0).apply(lambda x: float(x))
                master['rec_yt'] = master['rec_yt'].apply(lambda x: x.replace('','0') if (len(str(x))==0) | (len(str(x))==1) else x).fillna(0).apply(lambda x: float(x))
                master['rz_td_pct'] = master['rz_td_pct'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['rz_succ%'] = master['rz_succ%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['rec_trgts%'] = master['rec_trgts%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['rec_td%'] = master['rec_td%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['rec_yds%'] = master['rec_yds%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['proj_sacks'] = master['proj_sacks'].apply(lambda x: x.replace('','0') if (len(str(x))==0) | (len(str(x))==1) else x).fillna(0).apply(lambda x: float(x))
                master['pass_succ'] = master['pass_succ'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['rush_succ'] = master['rush_succ'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['takeaway%'] = master['takeaway%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['td%'] = master['td%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['ypp'] = master['ypp'].apply(lambda x: x.replace('','0') if (len(str(x))==0) | (len(str(x))==1) else x).fillna(0).apply(lambda x: float(x))
                master['rz_snaps'] = master['rz_snaps'].apply(lambda x: x.replace('','0') if (len(str(x))==0) | (len(str(x))==1) else x).fillna(0).apply(lambda x: float(x))
                master['rz_snaps10'] = master['rz_snaps10'].apply(lambda x: x.replace('','0') if (len(str(x))==0) | (len(str(x))==1) else x).fillna(0).apply(lambda x: float(x))
                master['rz_snaps5'] = master['rz_snaps5'].apply(lambda x: x.replace('','0') if (len(str(x))==0) | (len(str(x))==1) else x).fillna(0).apply(lambda x: float(x))
                master['TD%'] = master['TD%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)/100
                master['rec_TAY'] = master['rec_TAY'].astype(str).apply(lambda x: x.replace(' ','0') if len(x)==1 else x).fillna(0).apply(lambda x: float(x))
                master['rec_TAY%'] = master['rec_TAY%'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).apply(lambda x: x.replace('%','') if str(x)[-1]=='%' else x).fillna(0).astype(float)
                master['CAY'] = master['CAY'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).fillna(0).apply(lambda x: float(x))
                master['IAY'] = master['IAY'].apply(lambda x: x.replace(' ','0') if len(str(x))==1 else x).fillna(0).apply(lambda x: float(x))
                
                
                fd = pd.read_csv(os.getcwd() + r'\fd_mainline\_predict\player_stats\fanduel_files\{0}.csv'.format(we.replace('/','.')), header=6, index_col=13).iloc[:,13:]
                
                '''NEW'''
                fd['First Name'] = fd['First Name'].apply(lambda x: x.replace('-', ''))

                
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.lower())

                '''NEW'''
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace('st. ', ''))
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace('-', ''))
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace(' iii', ''))
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace(' ii', ''))
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace(' iv', ''))
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace(' v', '') if x.split(' ')[-1] == 'v' else x)
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace(' jr.', ''))
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace(' sr.', ''))
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace(' sr.', ''))
                fd['Last Name'] = fd['Last Name'].apply(lambda x: x.replace(' ', ''))
                fd['City Name'] = np.where(fd['Position'] == 'D', fd['Nickname'].apply(lambda x: x.split(' ')[1]), ['ryland'])
                fd['City Name2'] = fd['City Name'].apply(lambda x: 'NY' if x =='York' else  x)
                fd['City Name2'] = fd['City Name2'].apply(lambda x: 'LA' if x == 'Angeles' else  x)
                fd['City Name3'] = np.where((fd['City Name2'] == 'LA') | (fd['City Name2'] == 'NY'), fd['City Name2'].astype(str) + ' ' + fd['Last Name'], fd['First Name'])
                fd['City Name3'] = fd['City Name3'].str.lower()
                fd['First Name'] = fd['First Name'].str.lower().apply(lambda x: x.replace(' ', '')[0])
                fd['RylandID'] = np.where(fd['Position'] == 'D', fd['City Name3'] + fd['Salary'].astype(str), fd['Last Name'] + fd['Salary'].astype(str) + fd['Position'].str.lower() + fd['First Name'])

                fd.index = fd['RylandID']
                
                
                master['name'] = master['name'].apply(lambda x: x.replace(' Defense', ''))
                master['Last Name_master'] = master['name'].apply(lambda x: x.lower())
                master['City Name_master'] = master['name'].apply(lambda x: x.lower())

                '''NEW'''
                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace('st. ', ''))
                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace('-', ''))

                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' iii', ''))
                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' ii', ''))
                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' iv', ''))
                #master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' v', ''))
                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' jr.', ''))
                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' sr.', ''))
                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' sr.', ''))
                master['First Name_master'] = master['Last Name_master'].apply(lambda x: x.split(' ')[0])
                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.split(' ')[1] if len(x.split(' '))>1 else x.split(' ')[0])
                master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' ', ''))
                master['First Name_master'] = master['First Name_master'].str.lower().apply(lambda x: x.replace(' ', '')[0])
                master['RylandID_master'] = np.where(master['pos'] == 'DEF', master['City Name_master'] + + master['salary'].astype(str),  master['Last Name_master'] + master['salary'].astype(str) + master['pos'].str.lower() + master['First Name_master'])
                master['pos'] = np.where(master['pos']=='DEF','D',master['pos'])

                master.index = master['RylandID_master']
                
                
                master = master.join(fd)
                master = master.copy()

                master.to_csv(os.getcwd() + r"\fd_mainline\_predict\player_stats\by_week\{0}.csv".format(format(we.replace('/','.'))))
            
            except Exception as ex:
                print(ex)
                print(repr(ex))
                break

    
            
            







































