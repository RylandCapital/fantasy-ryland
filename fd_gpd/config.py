
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

cores = 40
gameday_week = '4.1.23'
gameday_optimal_proj = 156.4

historical_winning_scores = {  
 '1.6.22': {'day':'thursday', 'slate_id':0, 'winning_score':273.90, 'optimal':337.3},
 '1.8.22': {'day':'saturday', 'slate_id':1, 'winning_score':251.60, 'optimal':297.8},
 '1.13.22': {'day':'thursday', 'slate_id':2, 'winning_score':229.00, 'optimal':319.4},
 '1.15.22': {'day':'saturday', 'slate_id':3, 'winning_score':242.50, 'optimal':302},
 '1.20.22': {'day':'thursday', 'slate_id':4, 'winning_score':250.50, 'optimal':334},
 '1.22.22': {'day':'saturday', 'slate_id':5, 'winning_score':229.60, 'optimal':350},
 '1.27.22': {'day':'thursday', 'slate_id':6, 'winning_score':254.40, 'optimal':322.4},
 '1.29.22': {'day':'saturday', 'slate_id':7, 'winning_score':221.50, 'optimal':277.8},
 '2.10.22': {'day':'thursday', 'slate_id':8, 'winning_score':234.40, 'optimal':312.4},
 '2.12.22': {'day':'saturday', 'slate_id':9, 'winning_score':260.50, 'optimal':307.2},
 '2.17.22': {'day':'thursday', 'slate_id':10, 'winning_score':230.20, 'optimal':327.6},
 '2.19.22': {'day':'saturday', 'slate_id':11, 'winning_score':268.30, 'optimal':292},
 '2.24.22': {'day':'thursday', 'slate_id':12, 'winning_score':248.10, 'optimal':319.8},
 '2.26.22': {'day':'saturday', 'slate_id':13, 'winning_score':266.50, 'optimal':357.5},
 '3.3.22': {'day':'thursday', 'slate_id':14, 'winning_score':216.20, 'optimal':351.5},
 '3.5.22': {'day':'saturday', 'slate_id':15, 'winning_score':247.90, 'optimal':332.2},
 '3.10.22': {'day':'thursday', 'slate_id':16, 'winning_score':300.60, 'optimal':351},
 '3.12.22': {'day':'saturday', 'slate_id':17, 'winning_score':232.70, 'optimal':302.8},
 '3.17.22': {'day':'thursday', 'slate_id':18, 'winning_score':255.50, 'optimal':324.7},
 '3.19.22': {'day':'saturday', 'slate_id':19, 'winning_score':216.70, 'optimal':265.8},
 '3.24.22': {'day':'thursday', 'slate_id':20, 'winning_score':253.00, 'optimal':322.5},
 '3.26.22': {'day':'saturday', 'slate_id':21, 'winning_score':247.60, 'optimal':343.1},
 '3.31.22': {'day':'thursday', 'slate_id':22, 'winning_score':228.40, 'optimal':306.1},
 '4.2.22': {'day':'saturday', 'slate_id':23, 'winning_score':239.30, 'optimal':309.5},
 '4.9.22': {'day':'saturday', 'slate_id':24, 'winning_score':268.90, 'optimal':352.9},
 '4.14.22': {'day':'thursday', 'slate_id':25, 'winning_score':287.20, 'optimal':369.7},
 '4.16.22': {'day':'saturday', 'slate_id':26, 'winning_score':238.40, 'optimal':350.8},
 '10.20.22': {'day':'thursday', 'slate_id':29, 'winning_score':242.20, 'optimal':356.2},
 '10.22.22': {'day':'saturday', 'slate_id':30, 'winning_score':242.20, 'optimal':322.2}, 
 '10.27.22': {'day':'thursday', 'slate_id':31, 'winning_score':280.20, 'optimal':336.8},  
 '10.29.22': {'day':'saturday', 'slate_id':32, 'winning_score':235.90, 'optimal':325.1}, 
 '11.10.22': {'day':'thursday', 'slate_id':35, 'winning_score':281.80, 'optimal':363.1}, 
 '11.12.22': {'day':'saturday', 'slate_id':36, 'winning_score':196.70, 'optimal':296.1},
 '11.17.22': {'day':'thursday', 'slate_id':37, 'winning_score':279.60, 'optimal':363}, 
 '11.19.22': {'day':'saturday', 'slate_id':38, 'winning_score':286.10, 'optimal':336.3},
 '12.1.22': {'day':'thursday', 'slate_id':39, 'winning_score':258.40, 'optimal':354.9}, 
 '12.3.22': {'day':'saturday', 'slate_id':40, 'winning_score':234.80, 'optimal':327.6},
 '12.8.22': {'day':'thursday', 'slate_id':41, 'winning_score':219.40, 'optimal':264.2}, 
 '12.10.22': {'day':'saturday', 'slate_id':42, 'winning_score':233.40, 'optimal':286.4},
 '12.15.22': {'day':'thursday', 'slate_id':43, 'winning_score':232.50, 'optimal':295.6}, 
 '12.17.22': {'day':'saturday', 'slate_id':44, 'winning_score':222.70, 'optimal':318.6},
 '12.22.22': {'day':'thursday', 'slate_id':45, 'winning_score':211.10, 'optimal':297.8},
 '1.5.23': {'day':'thursday', 'slate_id':46, 'winning_score':245.60, 'optimal':325.3},
 '1.7.23': {'day':'saturday', 'slate_id':47, 'winning_score':238.30, 'optimal':338.6},
 '1.10.23': {'day':'tuesday', 'slate_id':48, 'winning_score':241.00, 'optimal':329.6},
 '1.12.23': {'day':'thursday', 'slate_id':49, 'winning_score':212.25, 'optimal':298.2},
 '1.14.23': {'day':'saturday', 'slate_id':50, 'winning_score':217.70, 'optimal':339},
 '1.17.23': {'day':'tuesday', 'slate_id':51, 'winning_score':207.10, 'optimal':324.6},
 '1.19.23': {'day':'thursday', 'slate_id':52, 'winning_score':227.00, 'optimal':315.1},
 '1.21.23': {'day':'saturday', 'slate_id':53, 'winning_score':193.00, 'optimal':314.2},
 '1.24.23': {'day':'tuesday', 'slate_id':54, 'winning_score':243.00, 'optimal':345.2},
 '1.26.23': {'day':'thursday', 'slate_id':55, 'winning_score':231.00, 'optimal':355.2},
 '2.7.23': {'day':'tuesday', 'slate_id':56, 'winning_score':209.00, 'optimal':273.2},
 '2.9.23': {'day':'thursday', 'slate_id':57, 'winning_score':231.00, 'optimal':309.8},
 '2.17.23': {'day':'friday', 'slate_id':58, 'winning_score':237.00, 'optimal':301.4}, #remove? 5 game slate
 '2.18.23': {'day':'saturday', 'slate_id':59, 'winning_score':258.00, 'optimal':332.8},
 '2.21.23': {'day':'tuesday', 'slate_id':60, 'winning_score':251.00, 'optimal':332.3},
 '2.23.23': {'day':'thursday', 'slate_id':61, 'winning_score':244.00, 'optimal':342.9},
 '2.25.23': {'day':'saturday', 'slate_id':62, 'winning_score':183.00, 'optimal':262.4},
 '2.28.23': {'day':'tuesday', 'slate_id':63, 'winning_score':244.00, 'optimal':381.9},
 '3.2.23': {'day':'thursday', 'slate_id':64, 'winning_score':226.00, 'optimal':319.9},
 '3.4.23': {'day':'saturday', 'slate_id':65, 'winning_score':222.00, 'optimal':311},
 '3.7.23': {'day':'tuesday', 'slate_id':66, 'winning_score':260.00, 'optimal':349.4},
 '3.9.23': {'day':'thursday', 'slate_id':67, 'winning_score':215, 'optimal':314},
 '3.11.23': {'day':'saturday', 'slate_id':68, 'winning_score':230, 'optimal':352},
 '3.14.23': {'day':'tuesday', 'slate_id':69, 'winning_score':260, 'optimal':353.9},
 '3.16.23': {'day':'thursday', 'slate_id':70, 'winning_score':224.10, 'optimal':327.4},
 '3.18.23': {'day':'saturday', 'slate_id':71, 'winning_score':252, 'optimal':348.9}, 
 '3.20.23': {'day':'monday', 'slate_id':72, 'winning_score':220.20, 'optimal':293}, #remove? 5 game slate
 '3.21.23': {'day':'tuesday', 'slate_id':73, 'winning_score':231.00, 'optimal':349.4},
 '3.23.23': {'day':'thursday', 'slate_id':74, 'winning_score':191.3, 'optimal':282.9}, 
 '3.25.23': {'day':'saturday', 'slate_id':75, 'winning_score':271.60, 'optimal':329.50},
 '3.27.23': {'day':'monday', 'slate_id':76, 'winning_score':227.30, 'optimal':300.4},
 '3.28.23': {'day':'tuesday', 'slate_id':77, 'winning_score':245.9, 'optimal':352.8},
 '3.30.23': {'day':'thursday', 'slate_id':78, 'winning_score':231.1, 'optimal':313.2},
}

master_historical_weeks = [
          
        ]

curr_historical_optimize_weeks = [
   ['3.30.23']
    ]

mlweeks = [1,2] 

#if shift == Trus, FantasyLabs scraper will use shifted columns to ensure accuracy
shift = False



