import pandas as pd
import time
import numpy as np
import os

from selenium.webdriver.common.keys import Keys

from fd_gpd._historical.player_stats import helpers


def pull_stats(slate_ids=[], strdates=[]):
    
        driver = helpers.load_window_fanduel()
        time.sleep(10)
        # sid = 16
        # date = '3/10/22'
  
        for date, sid in zip(strdates[0:], slate_ids):

            print('\n\n\ncurrently scraping date : {0}'.format(date))

            driver.get('https://www.fantasylabs.com/nhl/player-models/?date={0}'.format(date))
            time.sleep(5)
            driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[1]/a[1]').click()
            time.sleep(1)
            main_locate = pd.Series(['Main' in sub for sub in driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[2]').text.split('\n')])
            main_locate = main_locate[main_locate==True].index[0] + 1
            time.sleep(1)
            driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[7]/div[2]/div[{0}]'.format(main_locate)).click()
            time.sleep(5)
            
            #%%
            driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[1]/a').click()
            time.sleep(5)
            
            name = 'C'
            
            num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
            
            columns = []
            column_names = ['rating', 'name', 'salary', 'pos', 'min', 'max']
            for n, t in zip(column_names, np.arange(2,7)):
                column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                                                                    
                columns.append(column) 
            left = pd.concat(columns, axis=1) 

            rcs = []
            for i in np.arange(1,15):
                rc = driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/div[{0}]'.format(i)).text.split('\n')            
                rc2 = [(rc[0]+'_'+i).replace(' ','').lower() for i in rc]
                if i==2:
                    [rcs.append(l) for l in rc2]
                else:
                    [rcs.append(l) for l in rc2[1:]]
            rcolumns = []
            rcolumn_names = rcs
            len_names = len(rcolumn_names)
            for n, t in zip(rcolumn_names, np.arange(1,len_names+1)):
                try:
                    rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    rcolumns.append(rcolumn) 
                except:
                    rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    rcolumns.append(rcolumn) 
                    
            right = pd.concat(rcolumns, axis=1)  
            
            finalc = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
            finalc['slate_id'] = sid
            finalc.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))
        
            cdf = finalc.copy()
            
            #%%
            try:
                driver.refresh()
                time.sleep(10)
                driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[1]/a[1]').click()
                time.sleep(1)
                main_locate = pd.Series(['Main' in sub for sub in driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[2]').text.split('\n')])
                main_locate = main_locate[main_locate==True].index[0] + 1
                time.sleep(1)
                driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[7]/div[2]/div[{0}]'.format(main_locate)).click()
                time.sleep(5)
                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[2]/a').click()
                time.sleep(5)
                
                
                name = 'W'
                            
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                columns = []
                column_names = ['rating', 'name', 'salary', 'pos', 'min', 'max']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 

                rcs = []
                for i in np.arange(1,15):
                    rc = driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/div[{0}]'.format(i)).text.split('\n')            
                    rc2 = [(rc[0]+'_'+i).replace(' ','').lower() for i in rc]
                    if i==2:
                        [rcs.append(l) for l in rc2]
                    else:
                        [rcs.append(l) for l in rc2[1:]]
                rcolumns = []
                rcolumn_names = rcs
                len_names = len(rcolumn_names)
                for n, t in zip(rcolumn_names, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finalc = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finalc['slate_id'] = sid
                finalc.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))
            
                wdf = finalc.copy()
            except:
                driver.refresh()
                time.sleep(10)
                driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[1]/a[1]').click()
                time.sleep(1)
                main_locate = pd.Series(['Main' in sub for sub in driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[2]').text.split('\n')])
                main_locate = main_locate[main_locate==True].index[0] + 1
                time.sleep(1)
                driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[7]/div[2]/div[{0}]'.format(main_locate)).click()
                time.sleep(5)
                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[2]/a').click()
                time.sleep(5)
                
                
                name = 'W'
                            
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                columns = []
                column_names = ['rating', 'name', 'salary', 'pos', 'min', 'max']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 

                rcs = []
                for i in np.arange(1,15):
                    rc = driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/div[{0}]'.format(i)).text.split('\n')            
                    rc2 = [(rc[0]+'_'+i).replace(' ','').lower() for i in rc]
                    if i==2:
                        [rcs.append(l) for l in rc2]
                    else:
                        [rcs.append(l) for l in rc2[1:]]
                rcolumns = []
                rcolumn_names = rcs
                len_names = len(rcolumn_names)
                for n, t in zip(rcolumn_names, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finalc = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finalc['slate_id'] = sid
                finalc.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))
            
                wdf = finalc.copy()
        
            #%%
            try:
                driver.refresh()
                time.sleep(10)
                driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[1]/a[1]').click()
                time.sleep(1)
                main_locate = pd.Series(['Main' in sub for sub in driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[2]').text.split('\n')])
                main_locate = main_locate[main_locate==True].index[0] + 1
                time.sleep(1)
                driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[7]/div[2]/div[{0}]'.format(main_locate)).click()
                time.sleep(5)
                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[3]/a').click()
                time.sleep(5)

                name = 'D'
                    
                #this gets the little blue number that shows number of players in that position that day
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                columns = []
                column_names = ['rating', 'name', 'salary', 'pos', 'min', 'max']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 

                rcs = []
                for i in np.arange(1,15):
                    rc = driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/div[{0}]'.format(i)).text.split('\n')            
                    rc2 = [(rc[0]+'_'+i).replace(' ','').lower() for i in rc]
                    if i==2:
                        [rcs.append(l) for l in rc2]
                    else:
                        [rcs.append(l) for l in rc2[1:]]
                rcolumns = []
                rcolumn_names = rcs
                len_names = len(rcolumn_names)
                for n, t in zip(rcolumn_names, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finalc = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finalc['slate_id'] = sid
                finalc.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))

                ddf = finalc.copy()
            except:
                driver.refresh()
                time.sleep(10)
                driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[1]/a[1]').click()
                time.sleep(1)
                main_locate = pd.Series(['Main' in sub for sub in driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[2]').text.split('\n')])
                main_locate = main_locate[main_locate==True].index[0] + 1
                time.sleep(1)
                driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[7]/div[2]/div[{0}]'.format(main_locate)).click()
                time.sleep(5)
                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[3]/a').click()
                time.sleep(5)

                name = 'D'
                    
                #this gets the little blue number that shows number of players in that position that day
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                columns = []
                column_names = ['rating', 'name', 'salary', 'pos', 'min', 'max']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 

                rcs = []
                for i in np.arange(1,15):
                    rc = driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/div[{0}]'.format(i)).text.split('\n')            
                    rc2 = [(rc[0]+'_'+i).replace(' ','').lower() for i in rc]
                    if i==2:
                        [rcs.append(l) for l in rc2]
                    else:
                        [rcs.append(l) for l in rc2[1:]]
                rcolumns = []
                rcolumn_names = rcs
                len_names = len(rcolumn_names)
                for n, t in zip(rcolumn_names, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finalc = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finalc['slate_id'] = sid
                finalc.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))

                ddf = finalc.copy()
            
            
            #%%
            try:
                driver.refresh()
                time.sleep(10)
                driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[1]/a[1]').click()
                time.sleep(1)
                main_locate = pd.Series(['Main' in sub for sub in driver.find_element('xpath','/html/body/article/section[1]/div[1]/div[7]/div[2]').text.split('\n')])
                main_locate = main_locate[main_locate==True].index[0] + 1
                time.sleep(1)
                driver.find_element('xpath', '/html/body/article/section[1]/div[1]/div[7]/div[2]/div[{0}]'.format(main_locate)).click()
                time.sleep(5)
                driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/nav/ul/li[5]/a').click()
                time.sleep(5)
                
                name = 'G'
                
                #this gets the little blue number that shows number of players in that position that day
                num_players = int(driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[1]/div/div/ul/li[2]/a/span').text)
                
                #loop on for left columns
                #this loop gets the first 4 columns, starting at column 3 as you can see in
                #np.arange(3,7) below
                columns = []
                column_names = ['rating', 'name', 'salary', 'pos', 'min', 'max']
                for n, t in zip(column_names, np.arange(2,7)):
                    column = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                    columns.append(column) 
                left = pd.concat(columns, axis=1) 
        
                rcs = []
                for i in np.arange(1,15):
                    rc = driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/div[{0}]'.format(i)).text.split('\n')            
                    rc2 = [(rc[0]+'_'+i).replace(' ','').lower() for i in rc]
                    if i==2:
                        [rcs.append(l) for l in rc2]
                    else:
                        [rcs.append(l) for l in rc2[1:]]
                rcolumns = []
                rcolumn_names = rcs
                len_names = len(rcolumn_names)
                for n, t in zip(rcolumn_names, np.arange(1,len_names+1)):
                    try:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                    except:
                        rcolumn = pd.DataFrame([driver.find_element('xpath','/html/body/article/section[2]/section/div[4]/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/div[{0}]/div[{1}]'.format(i,t)).text for i in np.arange(1,num_players+1)], columns =[n]) #uses last 2 divs (row then column, for examplle its row 1 column)
                        rcolumns.append(rcolumn) 
                        
                right = pd.concat(rcolumns, axis=1)  
                
                finalc = pd.concat([left.reset_index(drop=True), right.reset_index(drop=True)], axis=1)
                finalc['slate_id'] = sid
                finalc.to_excel(r'C:\Users\rmathews\Downloads\{0}.xlsx'.format(name))
            
                gdf = finalc.copy() 
            except:
                pass

                
            #%%  
            '''CLEANING'''
            
            master = pd.concat([cdf, wdf, ddf, gdf], sort=False).reset_index(drop=True)
            master['opp'] = master['team_opp'].str.split('-').apply(lambda x: x[0])
            master['slate_id'] = master['slate_id'].astype(str)
            for i in master.columns:
                if i not in ['name']:
                    master[i] = master[i].str.replace('$','')
                    master[i] = master[i].str.replace('%','')
                    master[i] = master[i].str.replace('@','')
                    master[i] = master[i].str.replace(' ','')
                    master[i] = master[i].str.replace('  ','')
                    try:
                        master[i]=master[i].apply(lambda x: x.replace('','0') if len(str(x))==0 else x).fillna(0)
                    except:
                        pass

            master['lines_full'] = master['lines_full'].apply(lambda x: x[0])
            master['time_b2b'] = master['time_b2b'].apply(lambda x: x[0] if len(x)>0 else x)

            master.to_excel(r'C:\Users\rmathews\Downloads\master.xlsx')
            
            master['Last Name_master'] = master['name'].apply(lambda x: x.lower())
            master['City Name_master'] = master['name'].apply(lambda x: x.lower())
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace('st. ', ''))
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace('-', ''))
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' iii', ''))
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' ii', ''))
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' iv', ''))
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' v', ''))
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' jr.', ''))
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' sr.', ''))
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' sr.', ''))
            master['First Name_master'] = master['Last Name_master'].apply(lambda x: x.split(' ')[0])
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.split(' ')[1] if len(x.split(' '))>1 else x.split(' ')[0])
            master['Last Name_master'] = master['Last Name_master'].apply(lambda x: x.replace(' ', ''))
            master['First Name_master'] = master['First Name_master'].str.lower().apply(lambda x: x.replace(' ', '')[0])
            master['RylandID_master'] =  master['Last Name_master'] + master['salary'].astype(str) + master['pos'].str.lower() + master['First Name_master']
            master.index = master['RylandID_master']

            master.to_csv(os.getcwd() + r"\fd_gpd\_historical\player_stats\by_week\{0}.csv".format(format(sid)))


    
            
            
  






































