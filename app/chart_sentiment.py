import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import random

# Anthony Powell
def generate_sample_data(days=60):
    """Generate sample tweet sentiment data over time."""
    current_time = datetime.now()
    data = []
    
    # Generate data points for each hour
    for day in range(days):
        for hour in range(24):
            timestamp = current_time - timedelta(days=day, hours=hour)
            # Generate random sentiment scores (-1 to 1)
            sentiment = random.uniform(-1, 1)
            data.append({
                'timestamp': timestamp,
                'sentiment': sentiment,
                'tweet_count': random.randint(5, 50)  # Random number of tweets per hour
            })
    
    return pd.DataFrame(data)

def plot_sentiment_analysis(data, time_window):
    """
    Create sentiment analysis plot for specified time window
    time_window: '24h', '30d', or '60d'
    """
    plt.figure(figsize=(12, 6))
    
    # Filter data based on time window
    current_time = datetime.now()
    if time_window == '24h':
        delta = timedelta(days=1)
        title = 'Last 24 Hours Sentiment Analysis'
        x_label = 'Hour'
    elif time_window == '30d':
        delta = timedelta(days=30)
        title = '30 Days Sentiment Analysis'
        x_label = 'Date'
    else:  # 60d
        delta = timedelta(days=60)
        title = '60 Days Sentiment Analysis'
        x_label = 'Date'
    
    # Filter data
    start_time = current_time - delta
    filtered_data = data[data['timestamp'] >= start_time].copy()
    
    # Resample data based on time window
    if time_window == '24h':
        resampled = filtered_data.set_index('timestamp').resample('H').mean()
    else:
        resampled = filtered_data.set_index('timestamp').resample('D').mean()
    
    # Plot sentiment scores
    plt.plot(resampled.index, resampled['sentiment'], color='blue', label='Average Sentiment')
    
    # Color regions based on sentiment
    plt.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    plt.fill_between(resampled.index, resampled['sentiment'], 0,
                    where=(resampled['sentiment'] >= 0),
                    color='green', alpha=0.3, label='Positive Sentiment')
    plt.fill_between(resampled.index, resampled['sentiment'], 0,
                    where=(resampled['sentiment'] < 0),
                    color='red', alpha=0.3, label='Negative Sentiment')
    
    # Customize plot
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel('Sentiment Score')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt.gcf()

# Elali McNair
def create_sentiment_charts(time_windows=['24h', '30d', '60d']):
    """Create sentiment charts for all specified time windows."""
    # Generate sample data for 60 days (covers all windows)
    data = generate_sample_data(60)
    
    # Create charts for each time window
    charts = {}
    for window in time_windows:
        fig = plot_sentiment_analysis(data, window)
        charts[window] = fig
    
    return charts