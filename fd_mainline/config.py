
historical_winning_scores = {     
'1':241.96,
'2':205.32,
'3':238.54,
'4':216.78,
'5':285.64,
'6':215.80,
'7':214.86,
'8':225.86,
'9':233.52,
'10':218.92,
'11':197.74,
'12':225.18,
'13':188.66,
'14':206.46,
'15':232.00,
'16':234.00, #week 16 2019
'17':215.46, #week 1 2020
'18':223.60, #week 2 2020
'19':214.90, #week 3 2020
'20':232.00, #week 4 2020
'21':205.00, #week 5 2020
'22':208.00, #week 6 2020
'23':235.00, #week 7 2020
'24':211.24, #week 8 2020
'25':201.16, #week 9 2020
'26':196.06, #week 10 2020
'27':187.96, #week 11 2020
'28':230, #week 12 2020
'29':220, #week 13 2020
'30':220, #week 14 2020 
'31':199, #week 1 2021
'32':227, #week 2 2021
'33':204, #week 3 2021
'34':233, #week 4 2021
'35':231, #week 5 2021
'36':210, #week 6 2021 
'37':208, #week 7 2021 FL: 10/20/21
'38':190, #week 8 2021 FL: 10/27/21 
'39':196, #week 9 2021 FL: 11/03/21
'40':184, #week 10 2021 FL: 11/10/21
'41':221, #week 11 2021 FL: 11/17/21
'42':196, #week 12 2021 FL: 11/24/21
'43':219, #week 13 2021 FL: 12/01/21
'44':201, #week 14 2021 FL: 12/08/21
'45':186, #week 15 2021 FL: 12/15/21
'46':221, #week 1 2022 FL: 9/7/22
'47':245, #week 2 2022 FL: 9/14/22
'48':190, #week 3 2022 FL: 9/21/22
'49':228, #week 4 2022 FL: 9/28/22
'50':228, #week 5 2022 FL: 10/5/22
'51':198, #week 6 2022 FL: 10/12/22  
'52':215, #week 7 2022 FL: 10/19/22 
}

master_historical_weeks = [
          [1,2],[3,4],[5,6],[7,8],[9,10],[11,12],
          [13,14],[15,16],[17,18],[19,20],[21,22],[23,24],
          [25,26],[27,28],[29,30],[31,32], [33,34],[35,36],
          [37,38],[39,40],[41,42],[43,44],[45,46],[47,48],
          [49,50],[51,52]
        ]

curr_historical_optimize_weeks = [
    [51]
    ]

mlweeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,
          24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,
          44,45,46,47,48,49,50,51,52] 

#if shift == Trus, FantasyLabs scraper will use shifted columns to ensure accuracy
shift = False

gameday_week = '10.26.22'

rbcolumns_hist =  ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own',
                   'act_pts', 'impld_pts', 'lev_rank', 'leverage', 'sr', 'buzz',
                     'pro', 'my', 'bargain', 'opp+-', 'snaps', 'pts', 'opppts',
                     'delta', 'spread', 'o/u', 'spread%', 'rush_td%', 'rush_yards%',
                     'snaps%', 'rush_att', 'not sure', 'rush_yards',  'rush_y/a',
                     'rush_td', 'success', 'rec_trgts', 'not_sure2', 'rec_yards',
                     'rec_long', 'rec_yr', 'rec_td', 'rec_yt', 'rz_opp', 'rz_opp10',
                     'rz-opp5', 'rz_td_pct', 'rz_succ%', 'temp', 'humidity', 
                     'precip%', 'month_ppg', 'month_change', 'month_fpo', 'month_fps',
                     'consistency', 'upside', 'duds', 'count','year_ppg', 'year+-',
                     'year_change', 'year_fpo','year_fps', 'year_consistency', 
                     'year_upside', 'year_duds', 'year_count']

#flips impld_pts and act_pts, flips sr and buzz
rbcolumns_hist_shift =  ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own',
                   'impld_pts', 'act_pts', 'lev_rank', 'leverage', 'buzz', 'sr',
                     'pro', 'my', 'bargain', 'opp+-', 'snaps', 'pts', 'opppts',
                     'delta', 'spread', 'o/u', 'spread%', 'rush_td%', 'rush_yards%',
                     'snaps%', 'rush_att', 'not sure', 'rush_yards',  'rush_y/a',
                     'rush_td', 'success', 'rec_trgts', 'not_sure2', 'rec_yards',
                     'rec_long', 'rec_yr', 'rec_td', 'rec_yt', 'rz_opp', 'rz_opp10',
                     'rz-opp5', 'rz_td_pct', 'rz_succ%', 'temp', 'humidity', 
                     'precip%', 'month_ppg', 'month_change', 'month_fpo', 'month_fps',
                     'consistency', 'upside', 'duds', 'count','year_ppg', 'year+-',
                     'year_change', 'year_fpo','year_fps', 'year_consistency', 
                     'year_upside', 'year_duds', 'year_count']

wrcolumns_hist =  ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own',
                     'act_pts', 'impld_pts', 'lev_rank', 'leverage', 'sr', 'buzz',
                     'pro', 'my', 'bargain', 'opp+-', 'snaps', 'pts', 'opppts',
                     'delta', 'spread', 'o/u', 'spread%', 'rec_trgts%', 'rec_td%',
                     'rec_yds%', 'rec_trgts', 'not_sure2', 'rec_yards',
                     'rec_long', 'rec_yr', 'rec_td', 'rec_yt', 'rec_TAY', 'rec_TAY%', 'rz_opp', 'rz_opp10',
                     'rz-opp5', 'rz_td_pct', 'temp', 'humidity', 
                     'precip%', 'month_ppg', 'month_change', 'month_fpo', 'month_fps',
                     'consistency', 'upside', 'duds', 'count','year_ppg', 'year+-',
                     'year_change', 'year_fpo','year_fps', 'year_consistency', 
                     'year_upside', 'year_duds', 'year_count']

#flips impld_pts and act_pts, flips sr and buzz
wrcolumns_hist_shift =  ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own',
                     'impld_pts', 'act_pts', 'lev_rank', 'leverage', 'buzz', 'sr',
                     'pro', 'my', 'bargain', 'opp+-', 'snaps', 'pts', 'opppts',
                     'delta', 'spread', 'o/u', 'spread%', 'rec_trgts%', 'rec_td%',
                     'rec_yds%', 'rec_trgts', 'not_sure2', 'rec_yards',
                     'rec_long', 'rec_yr', 'rec_td', 'rec_yt', 'rec_TAY', 'rec_TAY%', 'rz_opp', 'rz_opp10',
                     'rz-opp5', 'rz_td_pct', 'temp', 'humidity', 
                     'precip%', 'month_ppg', 'month_change', 'month_fpo', 'month_fps',
                     'consistency', 'upside', 'duds', 'count','year_ppg', 'year+-',
                     'year_change', 'year_fpo','year_fps', 'year_consistency', 
                     'year_upside', 'year_duds', 'year_count']

tecolumns_hist =  ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own',
                   'act_pts', 'impld_pts', 'lev_rank', 'leverage', 'sr', 'buzz', 
                     'pro', 'my', 'bargain', 'opp+-', 'snaps', 'pts', 'opppts',
                     'delta', 'spread', 'o/u', 'spread%', 'rec_trgts%', 'rec_td%',
                     'rec_yds%', 'rec_trgts', 'not_sure2', 'rec_yards',
                     'rec_long', 'rec_yr', 'rec_td', 'rec_yt', 'rec_TAY', 'rec_TAY%', 'rz_opp', 'rz_opp10',
                     'rz-opp5', 'rz_td_pct', 'temp', 'humidity', 
                     'precip%', 'month_ppg', 'month_change', 'month_fpo', 'month_fps',
                     'consistency', 'upside', 'duds', 'count','year_ppg', 'year+-',
                     'year_change', 'year_fpo','year_fps', 'year_consistency', 
                     'year_upside', 'year_duds', 'year_count']

#flips impld_pts and act_pts, flips sr and buzz
tecolumns_hist_shift =  ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own',
                   'impld_pts', 'act_pts', 'lev_rank', 'leverage', 'buzz', 'sr', 
                     'pro', 'my', 'bargain', 'opp+-', 'snaps', 'pts', 'opppts',
                     'delta', 'spread', 'o/u', 'spread%', 'rec_trgts%', 'rec_td%',
                     'rec_yds%', 'rec_trgts', 'not_sure2', 'rec_yards',
                     'rec_long', 'rec_yr', 'rec_td', 'rec_yt', 'rec_TAY', 'rec_TAY%', 'rz_opp', 'rz_opp10',
                     'rz-opp5', 'rz_td_pct', 'temp', 'humidity', 
                     'precip%', 'month_ppg', 'month_change', 'month_fpo', 'month_fps',
                     'consistency', 'upside', 'duds', 'count','year_ppg', 'year+-',
                     'year_change', 'year_fpo','year_fps', 'year_consistency', 
                     'year_upside', 'year_duds', 'year_count']

qbcolumns_hist =  ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own',
                  'act_pts', 'impld_pts','lev_rank', 'leverage', 'sr', 'buzz',  'pro', 'my',
                  'bargain', 'opp+-', 'snaps', 'pts', 'opppts', 'delta', 'spread', 'o/u', 'spread%',
                  'comp', 'att', 'yards', '%', 'y/a', 'adj ypa', 'td', 'long', 'CAY', 'IAY', '%rb',
                  '%wr', '%te', '%td', 'int%', 'sack%', 'rush-att', 'not sure', 'rush_yards', 'rush_y/a',
                  'rush_td', 'success', 'rz_opp', 'rz_opp10', 'rz-opp5', 'temp', 'humidity', 'precip%',
                  'month_ppg', 'month_change', 'month_fpo', 'month_fps', 'consistency', 'upside', 'duds',
                  'count', 'year_ppg', 'year+-', 'year_change', 'year_fpo', 'year_fps', 'year_consistency',
                  'year_upside', 'year_duds', 'year_count']

#flips impld_pts and act_pts, flips sr and buzz
qbcolumns_hist_shift =  ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own',
                  'impld_pts', 'act_pts','lev_rank', 'leverage', 'buzz', 'sr',  'pro', 'my',
                  'bargain', 'opp+-', 'snaps', 'pts', 'opppts', 'delta', 'spread', 'o/u', 'spread%',
                  'comp', 'att', 'yards', '%', 'y/a', 'adj ypa', 'td', 'long', 'CAY', 'IAY', '%rb',
                  '%wr', '%te', '%td', 'int%', 'sack%', 'rush-att', 'not sure', 'rush_yards', 'rush_y/a',
                  'rush_td', 'success', 'rz_opp', 'rz_opp10', 'rz-opp5', 'temp', 'humidity', 'precip%',
                  'month_ppg', 'month_change', 'month_fpo', 'month_fps', 'consistency', 'upside', 'duds',
                  'count', 'year_ppg', 'year+-', 'year_change', 'year_fpo', 'year_fps', 'year_consistency',
                  'year_upside', 'year_duds', 'year_count']

defcolumns_hist  = ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own', 'proj_sacks', 'act_pts',
               'impld_pts', 'lev_rank', 'leverage', 'sr', 'buzz', 'pro', 'my', 'bargain', 'opp+-', 'pts',
              'opppts', 'delta', 'spread', 'o/u', 'spread%', 'int%', 'pass_succ', 'rush_succ', 'sack%', 
              'takeaway%', 'td%', 'ypp', 'rz_snaps', 'rz_snaps10', 'rz_snaps5', 'TD%', 'temp', 'humidity',
              'precip%', 'month_ppg', 'month_change', 'consistency', 'upside', 'duds', 'count', 'year_ppg',
              'year+-', 'year_change', 'year_consistency', 'year_upside', 'year_duds', 'year_count']

#flips impld_pts and act_pts, flips sr and buzz
defcolumns_hist_shift  = ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own', 'proj_sacks', 'impld_pts',
               'act_pts', 'lev_rank', 'leverage', 'buzz', 'sr', 'pro', 'my', 'bargain', 'opp+-', 'pts',
              'opppts', 'delta', 'spread', 'o/u', 'spread%', 'int%', 'pass_succ', 'rush_succ', 'sack%', 
              'takeaway%', 'td%', 'ypp', 'rz_snaps', 'rz_snaps10', 'rz_snaps5', 'TD%', 'temp', 'humidity',
              'precip%', 'month_ppg', 'month_change', 'consistency', 'upside', 'duds', 'count', 'year_ppg',
              'year+-', 'year_change', 'year_consistency', 'year_upside', 'year_duds', 'year_count']




