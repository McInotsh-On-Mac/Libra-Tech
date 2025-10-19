from app.analyze_sentiment import clean_tweet, analyze_sentiment, format_cleaned_text

def test_sentiment_functions():
    """Test sentiment analysis functions without database"""
    
    test_tweets = [
        "I absolutely love this amazing movie! It's fantastic and brilliant!",
        "This film is terrible, boring and a complete waste of time. Horrible acting.",
        "The movie was okay, nothing special but decent entertainment.",
        "Incredible masterpiece! Breathtaking cinematography and outstanding performances.",
        "Disappointing and overrated. Poor dialogue and confusing plot.",
        "Fun and entertaining! Great for the whole family, very enjoyable.",
        "Worst movie ever! Painfully bad and unwatchable garbage.",
        "Beautiful and touching story. Heartwarming and well-acted drama.",
        "Average film. Not great but not terrible either. Just mediocre.",
        "Epic blockbuster! Thrilling action and spectacular visual effects!"
    ]
    
    print("🧪 Testing Sentiment Analysis Functions")
    print("=" * 70)
    
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    
    for i, tweet in enumerate(test_tweets, 1):
        print(f"\n🐦 Tweet {i}:")
        print(f"RAW: {tweet}")
        
        # Clean the tweet
        tokens = clean_tweet(tweet)
        cleaned_text = format_cleaned_text(tokens)
        print(f"CLEANED: {cleaned_text}")
        
        # Analyze sentiment
        sentiment, score, matched_words = analyze_sentiment(tokens)
        print(f"SENTIMENT: {sentiment} (Score: {score})")
        
        if matched_words:
            print(f"MATCHED WORDS: {', '.join(matched_words)}")
        else:
            print("MATCHED WORDS: No sentiment words found")
        
        sentiment_counts[sentiment] += 1
        print("-" * 60)
    
    # Summary
    total = len(test_tweets)
    print(f"\n📊 SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total Tweets Analyzed: {total}")
    print(f"Positive: {sentiment_counts['Positive']} ({sentiment_counts['Positive']/total*100:.1f}%)")
    print(f"Negative: {sentiment_counts['Negative']} ({sentiment_counts['Negative']/total*100:.1f}%)")
    print(f"Neutral: {sentiment_counts['Neutral']} ({sentiment_counts['Neutral']/total*100:.1f}%)")

if __name__ == "__main__":
    test_sentiment_functions()