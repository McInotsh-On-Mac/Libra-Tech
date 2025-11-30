import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from .db import execute_query

# Anthony Powell
def to_datetime_safe(timestamp):
    """Convert various timestamp formats to datetime, handling date objects."""
    if isinstance(timestamp, datetime):
        return timestamp
    elif hasattr(timestamp, 'date') and callable(timestamp.date):
        # It's a date object, convert to datetime
        return datetime.combine(timestamp, datetime.min.time())
    elif isinstance(timestamp, str):
        # Parse string to datetime
        return pd.to_datetime(timestamp)
    else:
        return pd.to_datetime(timestamp)

def fetch_sentiment_data_from_db(days=60):
    """Fetch actual tweet sentiment data from the database."""
    current_time = datetime.now()
    start_time = current_time - timedelta(days=days)
    
    # Query to fetch sentiment history from the database
    query = """
    SELECT 
        analyzed_at as timestamp,
        sentiment_score as sentiment,
        total_tweets_analyzed as tweet_count,
        positive_count,
        negative_count,
        neutral_count
    FROM movie_sentiment_history
    WHERE analyzed_at >= %s
    ORDER BY analyzed_at ASC
    """
    
    try:
        results = execute_query(query, (start_time,), fetch=True)
        
        if not results:
            print(f"No sentiment data found in database for the last {days} days. Using empty dataset.")
            return pd.DataFrame(columns=['timestamp', 'sentiment', 'tweet_count', 'positive_count', 'negative_count', 'neutral_count'])
        
        # Convert results to DataFrame
        data = []
        for row in results:
            # Convert timestamp to datetime if it's just a date
            timestamp = row[0]
            if hasattr(timestamp, 'date') and not hasattr(timestamp, 'time'):
                # It's a date object, convert to datetime
                timestamp = datetime.combine(timestamp, datetime.min.time())
            elif isinstance(timestamp, str):
                # Parse string to datetime
                timestamp = pd.to_datetime(timestamp)
            
            data.append({
                'timestamp': pd.to_datetime(timestamp),
                'sentiment': row[1],
                'tweet_count': row[2],
                'positive_count': row[3],
                'negative_count': row[4],
                'neutral_count': row[5]
            })
        
        df = pd.DataFrame(data)
        # Ensure timestamp is datetime type
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    except Exception as e:
        print(f"Error fetching sentiment data from database: {e}")
        return pd.DataFrame(columns=['timestamp', 'sentiment', 'tweet_count', 'positive_count', 'negative_count', 'neutral_count'])

def plot_sentiment_analysis(data, time_window):
    """
    Create sentiment analysis plot for specified time window
    time_window: '24h', '30d', or '60d'
    """
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
    
    # If no data in this window, return empty chart
    if len(filtered_data) == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No data available for this time period', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=14)
        ax.set_title(title)
        return fig
    
    # Create figure for line chart
    fig, ax = plt.subplots(figsize=(12, 6))

    # Calculate net sentiment (positive - negative) for each data point
    filtered_data['net_sentiment'] = filtered_data['positive_count'] - filtered_data['negative_count']
    
    # Sort by timestamp to ensure proper line ordering
    filtered_data = filtered_data.sort_values('timestamp')

    # Plot line graph with each analysis as a point
    ax.plot(filtered_data['timestamp'], filtered_data['net_sentiment'], color='blue', marker='o', linewidth=2, label='Net Sentiment (Pos-Neg)')
    ax.axhline(0, color='gray', linestyle='--', alpha=0.7)

    ax.set_title(f'{title} - Net Sentiment Over Time')
    ax.set_xlabel(x_label)
    ax.set_ylabel('Net Sentiment (Positive - Negative)')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    # Rotate x-axis labels for better readability
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    return fig

# Elali McNair
def create_sentiment_charts(time_windows=['24h', '30d', '60d']):
    """Create sentiment charts for all specified time windows using actual database data."""
    # Fetch actual tweet sentiment data from the database for 60 days (covers all windows)
    data = fetch_sentiment_data_from_db(60)
    
    # Create charts for each time window
    charts = {}
    for window in time_windows:
        fig = plot_sentiment_analysis(data, window)
        charts[window] = fig
    
    return charts