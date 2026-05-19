import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Load in master dataset
df = pd.read_csv('nfl_master_seasonal_stats_2025.csv')
conn = sqlite3.connect(':memory:')
df.to_sql('nfl_stats', conn, index=False)

# SQL Query to calculate the players with the "Most Bang for Buck"
sql_query = """
SELECT 
    player_display_name, 
    position, 
    Salary, 
    production_score,
    (production_score / (Salary / 1000000.0)) AS value_per_million
FROM nfl_stats
WHERE position IN ('QB', 'RB', 'WR', 'TE')
  AND Salary > 0
  AND production_score > 0
ORDER BY value_per_million DESC
"""

analysis_df = pd.read_sql_query(sql_query, conn)
conn.close()

# Scatter plot of Production Score vs. Salary,
plt.figure(figsize=(12, 8))
colors = {'QB': 'tab:red', 'RB': 'tab:blue', 'WR': 'tab:green', 'TE': 'tab:orange'}

# Plot each position as a separate color on scatterplot
for pos, color in colors.items():
    subset = analysis_df[analysis_df['position'] == pos]
    plt.scatter(subset['Salary'], subset['production_score'], 
                label=pos, color=color, alpha=0.7, edgecolors='w', s=60)

# Labels, title, legend, and grid
plt.title('NFL 2025: Production Score vs. Salary', fontsize=15)
plt.xlabel('Salary (USD)')
plt.ylabel('Production Score')
plt.legend(title='Position')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('nfl_value_scatter.png')

# Print the top 20 "Most Bang for your Buck" players
top_20 = analysis_df.head(20)
print("Top 20 'Most Bang for your Buck' Players")
print(top_20[['player_display_name', 'position', 'value_per_million']])