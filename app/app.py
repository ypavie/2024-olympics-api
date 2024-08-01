from fastapi import FastAPI
from app.utils import get_olympic_data

app = FastAPI()

@app.get("/olympics")
def get_olympics_data():
    data = get_olympic_data()
    return {"data": data}
