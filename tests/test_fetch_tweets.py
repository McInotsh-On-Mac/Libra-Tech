# Anthony Powell
# This test ensures fetch_tweets_for_ui exists and (when stubbed) returns a dict with success and tweets.

import app.fetch_tweets as fetch_mod

def test_fetch_tweets_for_ui_smoke(monkeypatch):
    # stub the real function to avoid network calls
    def fake_fetch(keyword, count=10):
        assert isinstance(keyword, str)
        return {"success": True, "tweets": [{"id": "1", "text": "sample"}], "count": count}

    monkeypatch.setattr(fetch_mod, "fetch_tweets_for_ui", fake_fetch)
    res = fetch_mod.fetch_tweets_for_ui("Dune", count=3)

    assert isinstance(res, dict)
    assert res.get("success") is True
    assert isinstance(res.get("tweets"), list)
    assert res.get("count") == 3