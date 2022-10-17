
'''each number represents a slate, and 0,1,2 represent TNF, SNF, and MNF'''
historical_winning_scores = {     

1: { 
  #TNF WINING SCORE
  0:200,
  #SNF WINING SCORE
  1:200,
  #MNF WINING SCORE
  2:200,
  #fantasy labs date
  'date':'X/X/XXXX'
},
2: { 
  0:200,
  1:200,
  2:200,
  'date':'X/X/XXXX'
},
3: { 
  0:200,
  1:200,
  2:200,
  'date':'X/X/XXXX'
},
4: { 
  0:200,
  1:200,
  2:200,
  'date':'X/X/XXXX'
},

}




























master_historical_weeks = [
          [1,2],[3,4],[5,6],[7,8],[9,10],[11,12],
          [13,14],[15,16],[17,18],[19,20],[21,22],[23,24],
          [25,26],[27,28],[29,30],[31,32], [33,34],[35,36],
          [37,38],[39,40],[41,42],[43,44],[45,46],[47,48],
          [49,50]
        ]

curr_historical_optimize_weeks = [
    [50]
    ]

mlweeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,
          24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,
          44,45,46,47,48,49,50] 

#if shift == Trus, FantasyLabs scraper will use shifted columns to ensure accuracy
shift = False

gameday_week = '10.12.22'

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




