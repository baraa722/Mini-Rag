from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/")
async def welcome():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return {
        "message": f"welcome to {app_name}, we are at version {app_version} :)"
    }
