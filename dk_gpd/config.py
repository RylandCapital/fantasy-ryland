
import os



#set up environment filepaths for gpd
user = os.getlogin()
path = 'C:\\Users\\{0}\\.fantasy-ryland\\'.format(user)
if os.path.exists(path) == False:
  os.mkdir(path)
  os.mkdir(path+'_historical\\')
  os.mkdir(path+'_historical\\gpd\\')
  os.mkdir(path+'_historical\\gpd\\optimized_team_pools')
  os.mkdir(path+'_historical\\gpd\\ml_datasets')
  os.mkdir(path+'_predict\\')
  os.mkdir(path+'_predict\\gpd\\')
  os.mkdir(path+'_predict\\gpd\\optmized_team_pools\\')
  os.mkdir(path+'_predict\\gpd\\ml_predictions\\')
  os.mkdir(path+'_predict\\gpd\\uploaded_gameday_tickets\\')
  os.mkdir(path+'_backtesting\\')

cores = 35
gameday_week = '1.28.23'

historical_winning_scores = {  
 '1/6/22': {'day':'thursday', 'slate_id':0, 'winning_score':190.00},
 '1/8/22': {'day':'saturday', 'slate_id':1, 'winning_score':208.00},
 '1/13/22': {'day':'thursday', 'slate_id':2, 'winning_score':195.00},
 '1/15/22': {'day':'saturday', 'slate_id':3, 'winning_score':189.00},
 '1/20/22': {'day':'thursday', 'slate_id':4, 'winning_score':200.00},
 '1/22/22': {'day':'saturday', 'slate_id':5, 'winning_score':203.00},
 '1/27/22': {'day':'thursday', 'slate_id':6, 'winning_score':203.00},
 '1/29/22': {'day':'saturday', 'slate_id':7, 'winning_score':182.00},
 '2/10/22': {'day':'thursday', 'slate_id':8, 'winning_score':200.00},
 '2/12/22': {'day':'saturday', 'slate_id':9, 'winning_score':223.00},
 '2/17/22': {'day':'thursday', 'slate_id':10, 'winning_score':230.00},
 '2/19/22': {'day':'saturday', 'slate_id':11, 'winning_score':201.00},
 '2/24/22': {'day':'thursday', 'slate_id':12, 'winning_score':205.00},
 '2/26/22': {'day':'saturday', 'slate_id':13, 'winning_score':250.00},
 '3/3/22': {'day':'thursday', 'slate_id':14, 'winning_score':194.00},
 '3/5/22': {'day':'saturday', 'slate_id':15, 'winning_score':213.00},
 '3/10/22': {'day':'thursday', 'slate_id':16, 'winning_score':250.00},
 '3/12/22': {'day':'saturday', 'slate_id':17, 'winning_score':186.00},
 '3/17/22': {'day':'thursday', 'slate_id':18, 'winning_score':200.00},
 '3/19/22': {'day':'saturday', 'slate_id':19, 'winning_score':182.00},
 '3/24/22': {'day':'thursday', 'slate_id':20, 'winning_score':198.00},
 '3/26/22': {'day':'saturday', 'slate_id':21, 'winning_score':212.00},
 '3/31/22': {'day':'thursday', 'slate_id':22, 'winning_score':218.00},
 '4/2/22': {'day':'saturday', 'slate_id':23, 'winning_score':191.00},
 '4/9/22': {'day':'saturday', 'slate_id':24, 'winning_score':209.00},
 '4/14/22': {'day':'thursday', 'slate_id':25, 'winning_score':236.00},
 '4/16/22': {'day':'saturday', 'slate_id':26, 'winning_score':227.00},
 '10/20/22': {'day':'thursday', 'slate_id':29, 'winning_score':211.00}, 
 '10/22/22': {'day':'saturday', 'slate_id':30, 'winning_score':186.00}, 
 '10/27/22': {'day':'thursday', 'slate_id':31, 'winning_score':230.00}, 
 '10/29/22': {'day':'saturday', 'slate_id':32, 'winning_score':190.00},
 '11/10/22': {'day':'thursday', 'slate_id':35, 'winning_score':218.00}, 
 '11/12/22': {'day':'saturday', 'slate_id':36, 'winning_score':163.00},
 '11/17/22': {'day':'thursday', 'slate_id':37, 'winning_score':229.00}, 
 '11/19/22': {'day':'saturday', 'slate_id':38, 'winning_score':228.00},
 '12/1/22': {'day':'thursday', 'slate_id':39, 'winning_score':245.00}, 
 '12/3/22': {'day':'saturday', 'slate_id':40, 'winning_score':212.00},
 '12/8/22': {'day':'thursday', 'slate_id':41, 'winning_score':173.00}, 
 '12/10/22': {'day':'saturday', 'slate_id':42, 'winning_score':202.00},
 '12/15/22': {'day':'thursday', 'slate_id':43, 'winning_score':190.00}, 
 '12/17/22': {'day':'saturday', 'slate_id':44, 'winning_score':220.00},
 '12/22/22': {'day':'thursday', 'slate_id':45, 'winning_score':190.00},
 '1/5/23': {'day':'thursday', 'slate_id':46, 'winning_score':204.00},
 '1/7/23': {'day':'saturday', 'slate_id':47, 'winning_score':202.00},
 '1/10/23': {'day':'tuesday', 'slate_id':48, 'winning_score':186.00},
 '1/12/23': {'day':'thursday', 'slate_id':49, 'winning_score':183.00},
 '1/14/23': {'day':'saturday', 'slate_id':50, 'winning_score':182.00},
 '1/17/23': {'day':'tuesday', 'slate_id':51, 'winning_score':184.00},
 '1/19/23': {'day':'thursday', 'slate_id':52, 'winning_score':190.00},
 '1/21/23': {'day':'saturday', 'slate_id':53, 'winning_score':193.00},
 '1/24/23': {'day':'tuesday', 'slate_id':54, 'winning_score':216.00},
 #slates to be added: 1/26/23
}

master_historical_weeks = [
          
        ]

curr_historical_optimize_weeks = [
    ['1/21/23'],['1/24/23']
    ]

mlweeks = [1,2] 

#if shift == Trus, FantasyLabs scraper will use shifted columns to ensure accuracy
shift = False



