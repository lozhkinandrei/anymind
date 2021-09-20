from fastapi.testclient import TestClient

from core.config import settings
from main import app

client = TestClient(app)


def test_get_tweets_by_hashtags():
    hashtag = "python"
    response = client.get(f"{settings.API_V1_STR}/tweets/hashtags/{hashtag}")

    assert response.status_code == 200
    assert len(response.json()) == 30


def test_get_tweets_by_hashtags_with_limit():
    hashtag = "twitter"
    limit = 10
    response = client.get(
        f"{settings.API_V1_STR}/tweets/hashtags/{hashtag}?limit={limit}"
    )

    assert response.status_code == 200
    assert len(response.json()) == limit


def test_get_tweets_by_users():
    user = "twitter"
    response = client.get(f"{settings.API_V1_STR}/tweets/users/{user}")

    assert response.status_code == 200
    assert len(response.json()) == 30


def test_get_tweets_by_users_with_limit():
    user = "twitter"
    limit = 15
    response = client.get(f"{settings.API_V1_STR}/tweets/users/{user}?limit={limit}")
    
    assert response.status_code == 200
    assert len(response.json()) == limit
