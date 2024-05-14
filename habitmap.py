import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os

# Initialize or load data
def load_data(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        return pd.read_csv(filename, index_col='date', parse_dates=True)
    else:
        # Start a new DataFrame if none exists or if it's empty
        new_df = pd.DataFrame({'count': []})
        new_df.index.name = 'date'
        return new_df

# Save data back to CSV
def save_data(df, filename):
    df.to_csv(filename)

# Add or update a habit
def add_update_habit(df, date, count):
    if date in df.index:
        df.at[date, 'count'] += count
    else:
        df.loc[date] = count
    return df

# Generate the heatmap
def plot_heatmap(df, year):
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    dates = pd.date_range(start, end)
    
    # Prepare data
    data = df.reindex(dates, fill_value=0)
    data['day_of_week'] = data.index.dayofweek
    data['week_of_year'] = data.index.isocalendar().week
    
    # Pivot for heatmap format
    pivot = data.pivot(index="week_of_year", columns="day_of_week", values="count")
    
    # Plotting
    plt.figure(figsize=(12, 3))
    plt.title(f'Activity Tracker - {year}')
    plt.xlabel('Day of the Week')
    plt.ylabel('Week of Year')
    plt.pcolormesh(pivot, cmap='Greens', edgecolors='gray', linewidth=2)
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.show()

# Example usage
filename = 'habits.csv'
df = load_data(filename)

# Update your habits here
today = pd.Timestamp.today().normalize()  # Normalize to remove time part
df = add_update_habit(df, today, 1)  # Log today's activity

save_data(df, filename)
plot_heatmap(df, today.year)
