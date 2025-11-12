import psycopg2
import os
from app.utils.env_loader import load_env
load_env()


def get_db_connection():
    """
    Returns a new psycopg2 connection using environment variables.
    """
    # Required environment variables
    required_vars = ["DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432"))  
    )

def execute_query(query, params=None, fetch=False):
    """
    Executes a query on the PostgreSQL database.
    If fetch is True, returns fetched results.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    result = None
    if fetch:
        result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result

def initialize_tables():
    """
    Creates necessary tables if they do not exist.
    """
    # (Jania) Create user authentication table
    user_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """
    execute_query(user_table)

    # (Elali) Create movie sentiment history table
    movie_sentiment_history = """
    CREATE TABLE IF NOT EXISTS movie_sentiment_history (
        id SERIAL PRIMARY KEY, -- Auto-incrementing primary key
        movie_name VARCHAR(255) NOT NULL,
        overall_sentiment VARCHAR(255) NOT NULL,
        total_tweets_analyzed INTEGER NOT NULL DEFAULT 0,
        positive_count INTEGER NOT NULL DEFAULT 0,
        negative_count INTEGER NOT NULL DEFAULT 0,
        neutral_count INTEGER NOT NULL DEFAULT 0,
        positive_percentage DECIMAL (5,2) NOT NULL DEFAULT 0.0,
        negative_percentage DECIMAL (5,2) NOT NULL DEFAULT 0.0,
        neutral_percentage DECIMAL (5,2) NOT NULL DEFAULT 0.0,
        sentiment_score DECIMAL (8,3) NOT NULL DEFAULT 0.0,
        analyzed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
    );
    """
    execute_query(movie_sentiment_history)