from twitter_setup import client #import your twitter API client

def test_twitter_access():
    #try fetching your own tweets to check if API is still working
    try:
        response = client.get_users_tweets(id="1886950279301541888", max_results=5)
        if response.data:
            for i, tweet in enumerate(response.data, start=1):
                print(f"{i}. {tweet.text}\n")
        else:
            print("No tweets found.")
    except Exception as e:
        print(f"Error: {e}")

#run the test
test_twitter_access()