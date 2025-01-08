from fastapi import FastAPI
from routes.base import base_router
from dotenv import load_dotenv

# default path is .env, you can change it as you like
load_dotenv()

app = FastAPI()
app.include_router(base_router)
