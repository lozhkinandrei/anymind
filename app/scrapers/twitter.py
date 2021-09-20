import math
import re
import time
import json

import requests

from core.config import settings


class Twitter:
    """Simple twitter scraper implementation."""

    def __init__(self):
        self.URL = "https://twitter.com/i/api/2/search/adaptive.json"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {settings.TWITTER_AUTH_TOKEN}",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36",
            }
        )
        # update session guest twitter token each time new Twitter instance is initialized
        self.update_session_guest_token()

    def get_guest_token(self):
        """
            Gets Twitter's guest token from a response.text that is going
            to be used in every other request to Twitter's API.

        Returns:
            str: Guest token if match found else None
        """

        response = self.session.get("https://twitter.com")
        match = re.search("(?<=gt=)[0-9]*", response.text)

        if match:
            return match[0]

        return None

    def update_session_guest_token(self):
        token = self.get_guest_token()
        self.session.headers.update({"x-guest-token": token})

    def get_cursor(self, text):
        """
            Gets a cursor from the response.text that is used as a pagination
            in Twitter's search.

        Args:
            text (str): Text of the response.

        Returns:
            str: Cursor string if match found else None.
        """

        match = re.search('scroll:.*(?=","cursorType")', text)

        if match:
            return match[0]

        return None

    def format_tweet(self, tweet, user):
        """
            Format tweets received from Twitter API to match a format in Anymind
            test assignment specs.

        Args:
            tweet (dict): Dictionary containing tweet's data.
            user (dict): Dictionary containing creator's data of the tweet.

        Returns:
            dict: Dictionary that matches Anymind response format.
        """
        formatted_tweet = {
            "account": {
                "fullname": user.get("name"),
                "href": f"/{user.get('screen_name')}",
                "id": user.get("id"),
            },
            "date": tweet.get("created_at"),
            "hashtags": [
                "#" + hashtag["text"] for hashtag in tweet["entities"]["hashtags"]
            ],
            "likes": tweet.get("favorite_count"),
            "replies": tweet.get("reply_count"),
            "retweets": tweet.get("retweet_count"),
            "text": tweet.get("full_text"),
        }

        return formatted_tweet

    def get_tweets(self, hashtags=[], users=[], limit=30, cursor=None):
        """Returns a list of tweets with the given hashtags or/and from the given users.

        # Args:
            hashtags (list): Hashtags used in the search (e.g. ['#python', '#django']).
            users (list): Users whose feeds will be used in the search.
            limit (int, optional): Number of tweets to be returned.
            cursor (str): Twitter's API scroll to the next page.

        Returns:
            Dictionary containing "status_code" and "data" if status_code == 200 else "reason"
        """

        # format users list to twitter search format, e.g. ['from: twitter', 'from: django']
        from_users = [f"from:{user}" for user in users]

        # append sharp sign (#) in the beginning of the hashtag if the user forgot to include it
        hashtags = [
            "#" + hashtag if hashtag[0] != "#" else hashtag for hashtag in hashtags
        ]

        params = {
            "query_source": "typed_query",
            "include_reply_count": 1,  # adds replies count (as per requirements)
            "tweet_mode": "extended",  # adds full text of the tweet (as per requirements)
            "q": f"{(' OR '.join(from_users))} {(' OR '.join(hashtags))} -filter:links -filter:replies",
            "count": 20,  # max tweets per request
        }

        # how many requests should be sent, if max count per request 20
        iterations = math.ceil(limit / 20)

        result = []

        for i in range(iterations):
            response = self.session.get(self.URL, params=params)
            params["cursor"] = self.get_cursor(response.text)

            if response.status_code == 200:
                tweets = response.json()["globalObjects"]["tweets"]
                users = response.json()["globalObjects"]["users"]

                for key in tweets.keys():
                    if len(result) < limit:
                        tweet = tweets[key]
                        user = users[tweets[key]["user_id_str"]]
                        formatted_tweet = self.format_tweet(tweet, user)
                        result.append(formatted_tweet)
                    else:
                        return {"status_code": 200, "data": result}
            else:
                return {"status_code": response.status_code, "reason": response.reason}

        return {"status_code": 200, "data": result}
