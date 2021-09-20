from fastapi import APIRouter

from api.v1.endpoints import tweets

api_v1_router = APIRouter()
api_v1_router.include_router(tweets.router, prefix="/tweets", tags=["tweets"])
