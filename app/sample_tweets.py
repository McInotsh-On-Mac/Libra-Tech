# Elali McNair
import random
from datetime import datetime, timedelta

def generate_sample_tweets(keyword, count=6):
    """Generate sample tweets about movies with varying sentiment"""
    
    positive_templates = [
        "Just watched {movie}! Absolutely amazing! 🌟🌟🌟🌟🌟 #MustWatch",
        "Can't stop thinking about {movie} - best film I've seen this year! 🎬❤️",
        "{movie} exceeded all my expectations. Brilliant performance! #MovieNight",
        "The visuals in {movie} are breathtaking. A true masterpiece! ✨",
        "Finally saw {movie} and wow! The storyline is incredible! #Recommended",
        "Mind blown by {movie}! The directing is phenomenal 🎥 #Cinema",
    ]
    
    negative_templates = [
        "{movie} was disappointing... Expected much better 😕 #MovieReview",
        "Save your money - {movie} isn't worth the ticket price 😑",
        "Couldn't even finish watching {movie}. So boring! #Skip",
        "The plot of {movie} made no sense. What a letdown 👎",
        "{movie} was overhyped. Nothing special about it #Meh",
        "Wasted 2 hours watching {movie}. Don't recommend 🤦‍♂️",
    ]
    
    neutral_templates = [
        "{movie} was okay. Some good moments, some bad ones. #Neutral",
        "Mixed feelings about {movie}. Interesting concept but meh execution",
        "{movie} - decent entertainment but nothing spectacular 🤔",
        "Not sure how to feel about {movie}. Need to process it more.",
        "The reviews for {movie} are split and I can see why. #MovieThoughts",
        "{movie} had potential but didn't quite hit the mark",
    ]
    
    # Current timestamp for tweet creation
    now = datetime.now()
    
    tweets = []
    for i in range(count):
        # Randomly select sentiment and corresponding template
        sentiment = random.choice(['positive', 'negative', 'neutral'])
        if sentiment == 'positive':
            template = random.choice(positive_templates)
        elif sentiment == 'negative':
            template = random.choice(negative_templates)
        else:
            template = random.choice(neutral_templates)
            
        # Format tweet with movie name
        tweet_text = template.format(movie=keyword)
        
        # Create tweet object with metadata
        tweet = {
            'text': tweet_text,
            'created_at': (now - timedelta(hours=random.randint(0, 24))).isoformat(),
            'id': random.randint(1000000000, 9999999999),
            'user': {
                'screen_name': f'moviefan_{random.randint(100, 999)}',
                'followers_count': random.randint(50, 5000)
            },
            'retweet_count': random.randint(0, 100),
            'favorite_count': random.randint(0, 200)
        }
        tweets.append(tweet)
    
    return {
        'success': True,
        'tweets': tweets,
        'message': f'Generated {count} sample tweets for "{keyword}"'
    }