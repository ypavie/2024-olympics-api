from fastapi import FastAPI
from app.utils import get_olympic_data

app = FastAPI()

@app.get("/count")
def get_count():
    return {"count": 1}

@app.get("/olympics")
def get_olympics_data():
    data = get_olympic_data()
    return {"data": data}
