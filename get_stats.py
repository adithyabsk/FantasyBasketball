#!/usr/bin/env python
import json
import pandas as pd
import matplotlib.pyplot as plt
from nba_py import player
from datetime import datetime
from tqdm import tqdm

now = datetime.now()
now_str = now.strftime('%Y_%m_%d')
file_name = 'nba_data_{}.h5'.format(now_str)

print('Getting list of active players on {}'.format(now_str))
player_df = player.PlayerList(season='2017-18').info()
print('Serializing player list...')
player_df.to_hdf(file_name, 'player_data', mode='w', format='table')
player_ids = list(player_df['PERSON_ID'])


print('Getting logs for every player...')
player_logs = pd.DataFrame()
for p_id in tqdm(player_ids):
	# tqdm.write(player_df.loc[player_df['PERSON_ID'] == p_id, 'DISPLAY_LAST_COMMA_FIRST'].values[0])
	player_log = player.PlayerGameLogs(p_id, season='2017-18').info()
	player_log['FANTASY'] = player_log.PTS + \
							 player_log.STL * 3 + \
							 player_log.REB * 1.2 + \
							 player_log.FGM + \
							 player_log.FTM + \
							 player_log.BLK * 3 + \
							 player_log.AST * 1.5 + \
							 player_log.TOV * -1 + \
							 player_log.FGA * -1 + \
							 player_log.FTA * -1
	player_logs = player_logs.append(player_log, ignore_index=True)
print('Serializing player logs...')
player_df.to_hdf(file_name, 'player_logs', mode='a', format='table')