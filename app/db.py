import psycopg2
import os
from dotenv import load_dotenv

# TODO(Jania):(User Auth DB Migration): Set up connection utility and environment variable handling.
# TODO(Elali):(Tweets & Sentiment DB Migration): Add functions for tweets and sentiment database access.

load_dotenv()
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
    user_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """
    execute_query(user_table)
    
    sentiment_table = """
    CREATE TABLE IF NOT EXISTS sentiments (
        tweet_id SERIAL PRIMARY KEY,
        score INT NOT NULL, 
        label VACHAR(255)
    );
    """
    execute_query(sentiment_table)

    tweets_table = """
    CREATE TABLE IF NOT EXISTS tweets (
        tweet_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        content VARCHAR(255),
        timestamp TIMESTAMP
    );
    """
    execute_query(tweets_table)
    
