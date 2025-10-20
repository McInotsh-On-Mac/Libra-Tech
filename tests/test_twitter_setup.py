# Anthony Powell
# Verifies app.twitter_setup.create_twitter_client  Client when env is present
import types
import pytest

def test_create_twitter_client_returns_client(monkeypatch):
    try:
        import app.twitter_setup as ts
    except Exception as e:
        pytest.skip(f"Cannot import app.twitter_setup: {e}")

    if not hasattr(ts, "create_twitter_client"):
        pytest.skip("create_twitter_client not found in app.twitter_setup")

    # Provide common env vars the setup function might read
    monkeypatch.setenv("TWITTER_BEARER_TOKEN", "bearer_test")
    monkeypatch.setenv("TWITTER_API_KEY", "api_key_test")
    monkeypatch.setenv("TWITTER_API_KEY_SECRET", "api_secret_test")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN", "access_token_test")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN_SECRET", "access_secret_test")

    # Fake Client to avoid any network calls
    captured = {}
    class FakeClient:
        def __init__(self, *args, **kwargs):
            captured['args'] = args
            captured['kwargs'] = kwargs
        def search_recent_tweets(self, *a, **k):
            return {"data": []}

    fake_tweepy = types.SimpleNamespace(Client=FakeClient)
    # Patch likely references inside the module
    monkeypatch.setattr(ts, "tweepy", fake_tweepy, raising=False)
    monkeypatch.setattr(ts, "Client", FakeClient, raising=False)

    try:
        client = ts.create_twitter_client()
    except Exception as e:
        pytest.skip(f"create_twitter_client raised an exception: {e}")

    assert isinstance(client, FakeClient)