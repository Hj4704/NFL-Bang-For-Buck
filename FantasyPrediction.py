import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

df_2025_stats = pd.read_csv('nfl_master_seasonal_stats_2025.csv')
df_schedule = pd.read_csv('nfl_schedule_2026.csv')
df_defensive_ratings = pd.read_csv('nfl_defensive_ratings.csv')

df_2025_stats = df_2025_stats[df_2025_stats['position'].isin(['QB', 'RB', 'WR', 'TE'])]