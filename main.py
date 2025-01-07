from fastapi import FastAPI

app = FastAPI()

@app.get('/welcome')
def welcome():
    return {
        "message": "welcome to mini rag app"
    }
