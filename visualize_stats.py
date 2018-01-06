#!/usr/bin/env python

import pandas as pd
from glob import glob
from datetime import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

print('Getting Player Stats...')
globs = glob('nba_stats_*')
files = [(datetime.strptime(f[10:20], '%Y_%m_%d'), f) for f in globs]
_, f_name = max(files)
print('Using {}...'.format(f_name))
p_stats = pd.read_hdf(f_name, 'p_stats')

MEDIAN = p_stats.nlargest(100, 'MEDIAN').reset_index(drop=True)
STDDEV_50 = p_stats[(p_stats['GAMES'] >= 10) & (p_stats['MEDIAN'] >= 20)].nsmallest(50, 'STD_DEV')
MIN_50 = p_stats[p_stats['GAMES'] >= 5].nlargest(50, 'MIN')

print(MEDIAN)