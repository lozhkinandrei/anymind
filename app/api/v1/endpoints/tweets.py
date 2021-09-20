from fastapi import APIRouter, Response

from scrapers.twitter import Twitter

router = APIRouter()


@router.get(
    "/hashtags/{hashtag}",
    responses={
        200: {
            "description": "Tweets with the requested hashtag #python",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "account": {
                                "fullname": "Raymond Hettinger",
                                "href": "/raymondh",
                                "id": 14159138,
                            },
                            "date": "12:57 PM - 7 Mar 2018",
                            "hashtags": ["#python"],
                            "likes": 169,
                            "replies": 13,
                            "retweets": 27,
                            "text": """Historically, bash filename pattern... """,
                        }
                    ]
                }
            },
        },
    },
)
def get_tweets_by_hashtag(hashtag: str, response: Response, limit: int = 30):
    """Get the list of tweets with the given hashtag.

    Args:
    - hashtag (str): Hashtag to be used while searching for tweets.
    - limit (int, optional): Number of tweets to be returned.

    Returns:
    - Matched tweets
    """

    twitter = Twitter()
    result = twitter.get_tweets(hashtags=[hashtag], limit=limit)

    if result.get('status_code') == 200:
        return result['data']
    else:
        response.status_code = result.get('status_code')
        return result['reason']


@router.get(
    "/users/{user}",
    responses={
        200: {
            "description": "Tweets that belong to a user with a username twitter",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "account": {
                                "fullname": "Twitter",
                                "href": "/twitter",
                                "id": 783214,
                            },
                            "date": "2:54 PM - 8 Mar 2018",
                            "hashtags": ["#InternationalWomensDay"],
                            "likes": 287,
                            "replies": 17,
                            "retweets": 70,
                            "text": """Powerful voices. Inspiring women.\n\n#InternationalWomensDay""",
                        }
                    ]
                }
            },
        },
    },
)
def get_user_tweets(user: str, response: Response, limit: int = 30):
    """Get the list of tweets that belong to a given user.

    Args:
    - user (str): Username to whom the tweets belongs to.
    - limit (int, optional): Number of tweets to be returned.

    Returns:
    - Matched tweets
    """

    twitter = Twitter()
    result = twitter.get_tweets(users=[user], limit=limit)

    if result.get('status_code') == 200:
        return result['data']
    else:
        response.status_code = result.get('status_code')
        return result['reason']
