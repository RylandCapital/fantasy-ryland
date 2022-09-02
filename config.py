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
'16':234.00,
'120':215.46,
'220':223.60,
'320':214.90,
'420':232.00,
'520':205.00,
'620':208.00,
'720':235.00,
'820':211.24,
'920':201.16,
'1020':196.06,
'1120':187.96,
'1220':230,
'1320':220, 
'1420':220, #GUESSES
'1520':220, #GUESSES
'121':220,
}

master_historical_weeks = [
          [1,2],[3,4],[5,6],[7,8],[9,10],[11,12],
          [13,14],[15,16],[120,220],[320,420],[520,620],[720,820],
          [920,1020],[1120,1220],[1320,1420],[1520]
        ]

curr_historical_optimize_weeks = [
    [121]
]


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

qbcolumns_hist =  ['', ' ', 'proj', 'ceil', 'floor', 'proj+-', 'pts/sal', 'proj_own',
                  'act_pts', 'impld_pts','lev_rank', 'leverage', 'sr', 'buzz',  'pro', 'my',
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




