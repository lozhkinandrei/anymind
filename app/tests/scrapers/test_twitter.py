from fastapi.testclient import TestClient

from core.config import settings
from scrapers.twitter import Twitter
from main import app


def test_get_guest_token():
    twitter = Twitter()
    guest_token = twitter.get_guest_token()
    assert len(guest_token) == 19


def test_update_session_guest_token():
    twitter = Twitter()
    initial_guest_token = twitter.session.headers.get("x-guest-token")

    twitter.update_session_guest_token()
    updated_guest_token = twitter.session.headers.get("x-guest-token")

    assert initial_guest_token != updated_guest_token


def test_get_cursor():
    twitter = Twitter()

    example_cursor = (
        "scroll:thGAVUV0VFVBYBFoDYke7OuMD6JxIYtAESY8LrAAAB9D-AYk3S8an8AAAAFBP6_"
        "n8XVZAEE_pvIFIWYAIT-nO14RUgARP5pZLlVRABE_ohCtVXEAET-XBvtNewBRP6SErslxAAE_"
        "mJP63XIAQT-VvKVdUQAhP6lxDE1yAGE_qSeDjUYAsT-oGH7lZgChP6VbjClyAAE_"
        "oWjl1WYAET-jKGx1VQABP6Mgw2lkAHE_nsPyoXEAAT-aa33BcQABP5ZulNVyAEE_"
        "RNtNWQAFhFbSFehWAiXoYBlRPUElDUzUoFQAVAAA="
    )
    example_response_text = f'{{"entryId": "sq-cursor-bottom","sortIndex": "0","content":{{"operation":{{"cursor":{{"value":"{example_cursor}","cursorType": "Bottom"}}}}'

    cursor = twitter.get_cursor(example_response_text)
    assert cursor == example_cursor


def test_format_tweet():
    twitter = Twitter()

    example_tweet = {
        "created_at": "Sun Sep 19 07:47:49 +0000 2021",
        "id": 1439496436408721412,
        "id_str": "1439496436408721412",
        "full_text": "555",
        "entities": {
            "hashtags": [{"text": "Thailand", "indices": [3, 12]}],
        },
        "user_id": 3062054052,
        "user_id_str": "3062054052",
        "retweet_count": 6,
        "favorite_count": 23,
        "reply_count": 0,
    }

    example_user = {
        "id": 5392522,
        "id_str": "5392522",
        "name": "NPR",
        "screen_name": "NPR",
    }

    expected = {
        "account": {
            "fullname": example_user["name"],
            "href": f"/{example_user['screen_name']}",
            "id": example_user["id"],
        },
        "date": example_tweet["created_at"],
        "hashtags": [
            "#" + hashtag["text"] for hashtag in example_tweet["entities"]["hashtags"]
        ],
        "likes": example_tweet["favorite_count"],
        "replies": example_tweet["reply_count"],
        "retweets": example_tweet["retweet_count"],
        "text": example_tweet["full_text"],
    }

    formatted = twitter.format_tweet(example_tweet, example_user)

    assert formatted == expected


def test_get_tweets_by_hashtags():
    twitter = Twitter()
    hashtags = ["#python", "#django"]

    tweets = twitter.get_tweets(hashtags=hashtags).get('data')

    results = []

    # check that at least one hashtag is in hashtags list above for every tweet
    for tweet in tweets:
        contains_hashtag = any(
            hashtag.lower() in hashtags for hashtag in tweet.get("hashtags")
        )
        results.append(contains_hashtag)

    assert all(results) == True


def test_get_tweets_by_users():
    twitter = Twitter()
    users = ["python", "django"]

    tweets = twitter.get_tweets(users=users).get('data')

    # check that creator of the tweet is one of the users in the users list above
    results = [tweet["account"]["href"][1:].lower() in users for tweet in tweets]
    assert all(results) == True


def test_get_tweets_limit():
    twitter = Twitter()

    hashtags = ["#python"]
    limits = [1, 5, 10, 30]

    assert all([len(twitter.get_tweets(hashtags=hashtags, limit=limit).get('data')) == limit for limit in limits])
