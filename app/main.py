from fastapi import FastAPI

from api.v1.router import api_v1_router
from core.config import settings


description = """
### ⚠️ Notes:
Please be aware that this project is using [standard 7 days search API](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview), meaning it can fetch tweets only for the past 7 days.
"""

app = FastAPI(
    title="AnyMind Group [Python Backend Developer]",
    description=description,
    version='1.0.0'
)


@app.get("/")
def hello_world():
    return {"Hello": "World"}


app.include_router(api_v1_router, prefix=settings.API_V1_STR)
