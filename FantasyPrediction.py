import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

df_2025_stats = pd.read_csv('nfl_master_seasonal_stats_2025.csv')
df_schedule = pd.read_csv('nfl_schedule_2026.csv')
df_defensive_ratings = pd.read_csv('nfl_defensive_ratings.csv')
df_2025_stats = df_2025_stats[df_2025_stats['position'].isin(['QB', 'RB', 'WR', 'TE'])]

def_lookup = dict(zip(df_defensive_ratings['team'], df_defensive_ratings['rank']))
global_avg_rank = df_defensive_ratings['rank'].mean()

team_opponents = {}
for team in df_schedule['home_team'].unique():
    home_opponents = df_schedule[df_schedule['home_team'] == team]['away_team'].tolist()
    away_opponents = df_schedule[df_schedule['away_team'] == team]['home_team'].tolist()
    team_opponents[team] = home_opponents + away_opponents

for index, row in df_2025_stats.iterrows():
    player_team = row['team']
    opponents = team_opponents.get(player_team, [])

ratings = [def_lookup.get(opp, global_avg_rank) for opp in opponents]
player_strength_of_schedule.append(np.mean(ratings))

df_2025_stats['2026_opponent_def_rating'] = player_strength_of_schedule