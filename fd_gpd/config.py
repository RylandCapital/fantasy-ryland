
#2022 season started october 12

historical_winning_scores = {  
 '1/6/22': {'day':'thursday', 'slate_id':0, 'winning_score':273.90},
 '1/8/22': {'day':'saturday', 'slate_id':1, 'winning_score':251.60},
 '1/13/22': {'day':'thursday', 'slate_id':2, 'winning_score':229.00},
 '1/15/22': {'day':'saturday', 'slate_id':3, 'winning_score':242.50},
 '1/20/22': {'day':'thursday', 'slate_id':4, 'winning_score':250.50},
 '1/22/22': {'day':'saturday', 'slate_id':5, 'winning_score':229.60},
 '1/27/22': {'day':'thursday', 'slate_id':6, 'winning_score':254.40},
 '1/29/22': {'day':'saturday', 'slate_id':7, 'winning_score':221.50},
 '2/10/22': {'day':'thursday', 'slate_id':8, 'winning_score':234.40},
 '2/12/22': {'day':'saturday', 'slate_id':9, 'winning_score':260.50},
 '2/17/22': {'day':'thursday', 'slate_id':10, 'winning_score':230.20},
 '2/19/22': {'day':'saturday', 'slate_id':11, 'winning_score':268.30},
 '2/24/22': {'day':'thursday', 'slate_id':12, 'winning_score':248.10},
 '2/26/22': {'day':'saturday', 'slate_id':13, 'winning_score':266.50},
 '3/3/22': {'day':'thursday', 'slate_id':14, 'winning_score':216.20},
 '3/5/22': {'day':'saturday', 'slate_id':15, 'winning_score':247.90},
 '3/10/22': {'day':'thursday', 'slate_id':16, 'winning_score':300.60},
 '3/12/22': {'day':'saturday', 'slate_id':17, 'winning_score':232.70},
 '3/17/22': {'day':'thursday', 'slate_id':18, 'winning_score':255.50},
 '3/19/22': {'day':'saturday', 'slate_id':19, 'winning_score':216.70},
 '3/24/22': {'day':'thursday', 'slate_id':20, 'winning_score':253.00},
 '3/26/22': {'day':'saturday', 'slate_id':21, 'winning_score':247.60},
 '3/31/22': {'day':'thursday', 'slate_id':22, 'winning_score':228.40},
 '4/2/22': {'day':'saturday', 'slate_id':23, 'winning_score':239.30},
 '4/9/22': {'day':'saturday', 'slate_id':24, 'winning_score':268.90},
 '4/14/22': {'day':'thursday', 'slate_id':25, 'winning_score':287.20},
 '4/16/22': {'day':'saturday', 'slate_id':26, 'winning_score':238.40},
 '10/20/22': {'day':'thursday', 'slate_id':29, 'winning_score':242.20}, 
 '10/22/22': {'day':'saturday', 'slate_id':30, 'winning_score':242.20}, 
 '10/27/22': {'day':'thursday', 'slate_id':31, 'winning_score':280.20}, 
 '10/29/22': {'day':'saturday', 'slate_id':32, 'winning_score':235.90}, 
 '11/10/22': {'day':'thursday', 'slate_id':35, 'winning_score':281.80}, 
 '11/12/22': {'day':'saturday', 'slate_id':36, 'winning_score':196.70},
 '11/17/22': {'day':'thursday', 'slate_id':37, 'winning_score':279.60}, 
 '11/19/22': {'day':'saturday', 'slate_id':38, 'winning_score':286.10},
 '12/1/22': {'day':'thursday', 'slate_id':39, 'winning_score':258.40}, 
 '12/3/22': {'day':'saturday', 'slate_id':40, 'winning_score':234.80},
 '12/8/22': {'day':'thursday', 'slate_id':41, 'winning_score':219.40}, 
 '12/10/22': {'day':'saturday', 'slate_id':42, 'winning_score':233.40},
 '12/15/22': {'day':'thursday', 'slate_id':43, 'winning_score':232.50}, 
 '12/17/22': {'day':'saturday', 'slate_id':44, 'winning_score':222.70},
 '12/22/22': {'day':'thursday', 'slate_id':45, 'winning_score':211.10},
}

master_historical_weeks = [
          ['1/6/22','1/8/22'],['1/13/22','1/15/22'],['1/20/22','1/22/22'],
          ['1/27/22','1/29/22'],['2/10/22','2/12/22'],['2/17/22','2/19/22'],
          ['2/24/22','2/26/22'],['3/3/22','3/5/22'],['3/10/22','3/12/22'],

          ['3/17/22','3/19/22'],['3/24/22','3/26/22'],['3/31/22','4/2/22'],
          ['4/9/22','4/14/22'],['4/16/22'],['10/20/22'],
          ['10/22/22','10/27/22'],['10/29/22'],['11/10/22'],

          ['11/12/22','11/17/22'],['11/19/22','12/1/22'],['12/3/22','12/8/22'],
          ['12/10/22','12/15/22'],['12/17/22','12/22/22']
        ]

curr_historical_optimize_weeks = [
    ['1/6/22']
    ]

mlweeks = [1,2] 

#if shift == Trus, FantasyLabs scraper will use shifted columns to ensure accuracy
shift = False

gameday_week = '12.14.22'

