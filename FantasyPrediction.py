import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

# Load in the datasets needed for the projections
df_2025_stats = pd.read_csv('nfl_master_seasonal_stats_2025.csv')
df_schedule = pd.read_csv('schedule_2026.csv')
df_defensive_ratings = pd.read_csv('defensive_ratings.csv')
df_2025_stats = df_2025_stats[df_2025_stats['position'].isin(['QB', 'RB', 'WR', 'TE'])]

# Create a dictionary of defensive ratings for each team
def_lookup = dict(zip(df_defensive_ratings['team'], df_defensive_ratings['rank']))
global_avg_rank = df_defensive_ratings['rank'].mean()

# Calculating the average defensive rating that each player has to go up against in the 2026 season
team_opponents = {}
for team in df_schedule['home_team'].unique():
    home_opponents = df_schedule[df_schedule['home_team'] == team]['away_team'].tolist()
    away_opponents = df_schedule[df_schedule['away_team'] == team]['home_team'].tolist()
    team_opponents[team] = home_opponents + away_opponents
player_sos = []
for idx, row in df_2025_stats.iterrows():
    player_team = row['team']
    opponents = team_opponents.get(player_team, [])
    if len(opponents) == 0:
        player_sos.append(global_avg_rank)
        continue
    ratings = [def_lookup.get(opp, global_avg_rank) for opp in opponents]
    player_sos.append(np.mean(ratings))
df_2025_stats['2026_opponent_def_rating'] = player_sos

# Train Gradient Boosting Regressor model to predict the production score for 2026 based on the 2025 production score and the average defensive rating
# The target variable is adjusted by the ratio of the opponent's defensive rating to the global average rank
X = df_2025_stats[['production_score', '2026_opponent_def_rating']]
Y = df_2025_stats['production_score'] * (df_2025_stats['2026_opponent_def_rating'] / global_avg_rank)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=42)
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Generate the 2026 projections for each player and save to a new .csv file
df_2025_stats['predictions_2026'] = model.predict(X).round(2)
output_df = df_2025_stats[['player_display_name', 'position', 'team', 'production_score', '2026_opponent_def_rating', 'predictions_2026']]
output_df.to_csv('nfl_projections_2026.csv', index=False)
print(output_df.sort_values(by='predictions_2026', ascending=False).head(25))