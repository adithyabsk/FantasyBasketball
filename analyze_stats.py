#!/usr/bin/env python

import numpy as np
import pandas as pd
from tqdm import tqdm
from glob import glob
from datetime import datetime

print('Getting Player Fantasy Data...')
globs = glob('nba_data_*')
files = [(datetime.strptime(f[9:19], '%Y_%m_%d'), f) for f in globs]
_, f_name = max(files)
p_list = pd.read_hdf(f_name, 'p_list')
p_logs = pd.read_hdf(f_name, 'p_logs')

p_ids = list(p_list['PERSON_ID'])
p_stats = pd.DataFrame.from_items([('ID', pd.Series([], dtype='int')),
								   ('NAME', pd.Series([], dtype='str')),
								   ('MIN', pd.Series([], dtype='float')),
								   ('1_QUART', pd.Series([], dtype='float')),
								   ('MEDIAN', pd.Series([], dtype='float')),
								   ('3_QUART', pd.Series([], dtype='float')),
								   ('MAX', pd.Series([], dtype='float')),
								   ('MEAN', pd.Series([], dtype='float')),
								   ('STD_DEV', pd.Series([], dtype='float'))])
print('Analyzing Player Fantasy Data...')

for p_id in tqdm(p_ids):
	scores = p_logs.loc[p_logs['Player_ID'] == p_id, 'FANTASY'].values
	p_stat = [p_id]
	p_stat.append(p_list.loc[p_list['PERSON_ID'] == p_id, 'DISPLAY_LAST_COMMA_FIRST'].values[0])
	if not scores.size:
		 p_stat.extend(list(np.zeros(7) + np.nan))
		 p_stats.loc[len(p_stats)] = p_stat
		 continue
	p_stat.append(min(scores))
	p_stat.extend(np.percentile(scores, [25 ,50, 75]))
	p_stat.append(max(scores))
	p_stat.append(np.mean(scores))
	p_stat.append(np.std(scores))
	p_stats.loc[len(p_stats)] = p_stat

print('Serializing Player Fantasy Data...')
now = datetime.now()
now_str = now.strftime('%Y_%m_%d')
file_name = 'nba_stats_{}.h5'.format(now_str)
p_stats.to_hdf(file_name, 'p_stats', mode='w', format='table')
