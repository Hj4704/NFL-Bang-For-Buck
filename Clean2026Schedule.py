import pandas as pd

# From original .csv file taakes only the 2026 season games and puts them into a new .csv file
df = pd.read_csv("original_games.csv", low_memory=False)
df_2026 = df[df['season'] == 2026]
df_2026.to_csv("new_games.csv", index=False)
preview_cols = ['game_id', 'season', 'week', 'gameday', 'away_team', 'home_team']
print(df_2026[preview_cols].head())