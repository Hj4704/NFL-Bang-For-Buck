import pandas as pd
import re

# Load in weekly stats dataset
input_file = 'stats_player_week_2025.csv'
df_weekly = pd.read_csv(input_file)

# Exclude some of the columns from being added together when
exclude = ['player_id', 'player_name', 'player_display_name', 'position', 
           'position_group', 'headshot_url', 'season', 'week', 
           'season_type', 'game_id', 'team', 'opponent_team']

# Define the numeric columns to sum up
numeric_cols = df_weekly.select_dtypes(include=['number']).columns.tolist()

# Sum up all numeric columns and create a new season totals
sum_cols = [c for c in numeric_cols if c not in exclude]
seasonal_df = df_weekly.groupby(['player_id', 'player_display_name', 'position', 'team'])[sum_cols].sum().reset_index()

# Load in salary dataset
salary_df = pd.read_csv('nfl_salaries_2025.csv') 

# Clean the data
def clean_key(n): 
    return re.sub(r'[^a-zA-Z0-9]', '', str(n)).lower()

# Merge the seasonal stats and salary datasets into one
seasonal_df['match_key'] = seasonal_df['player_display_name'].apply(clean_key)
salary_df['match_key'] = salary_df['Player'].apply(clean_key)
final_df = pd.merge(seasonal_df, salary_df[['match_key', 'Salary']], on='match_key', how='left')

# Calculate the production score for each player
final_df['production_score'] = (
    (final_df.get('passing_yards', 0) / 25) + 
    (final_df.get('passing_tds', 0) * 4) - 
    (final_df.get('passing_interceptions', 0) * 2) + 
    (final_df.get('rushing_yards', 0) / 10) + 
    (final_df.get('rushing_tds', 0) * 6) - 
    (final_df.get('rushing_fumbles_lost', 0) * 2) + 
    (final_df.get('receiving_yards', 0) / 10) + 
    (final_df.get('receiving_tds', 0) * 6) + 
    (final_df.get('receptions', 0))
)

# Export final master dataset to a new .csv file
final_df.to_csv('nfl_master_seasonal_stats_2025.csv', index=False)
print("Done")