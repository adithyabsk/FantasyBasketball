#!/usr/bin/env python

import pandas as pd
from nba_py import player
from datetime import datetime
from tqdm import tqdm

now = datetime.now()
now_str = now.strftime('%Y_%m_%d')
file_name = 'nba_data_{}.h5'.format(now_str)

print('Getting list of active players on {}'.format(now_str))
p_list = player.PlayerList(season='2017-18').info()
print('Serializing player list...')
p_list.to_hdf(file_name, 'p_list', mode='w', format='table')
p_ids = list(p_list['PERSON_ID'])


print('Getting logs for every player...')
p_logs = pd.DataFrame()
for p_id in tqdm(p_ids):
	# tqdm.write(p_list.loc[p_list['PERSON_ID'] == p_id, 'DISPLAY_LAST_COMMA_FIRST'].values[0])
	p_logs = p_logs.append(player.PlayerGameLogs(p_id, season='2017-18').info(), ignore_index=True)
print('Computing Fantasy Score...')
p_logs[p_logs.columns.difference(['GAME_DATE', 'MATCHUP', 'WL'])] = p_logs[p_logs.columns.difference(['GAME_DATE', 'MATCHUP', 'WL'])].apply(pd.to_numeric)
p_logs['FANTASY'] = p_logs.PTS + \
						  	p_logs.STL * 3 + \
						  	p_logs.REB * 1.2 + \
						  	p_logs.FGM + \
						  	p_logs.FTM + \
						  	p_logs.BLK * 3 + \
						  	p_logs.AST * 1.5 + \
						  	p_logs.TOV * -1 + \
						  	p_logs.FGA * -1 + \
						  	p_logs.FTA * -1
print('Serializing player logs...')
p_logs.to_hdf(file_name, 'p_logs', mode='a', format='table')