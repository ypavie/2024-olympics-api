from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from typing import Optional
from app.utils import get_medal_summary

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <body>
            <h1>Welcome to the API</h1>
            <p>This is an API for retrieving Olympic data.</p>
            <h2>Default Values:</h2>
            <ul>
                <li>Event: Olympics 2024</li>
                <li>Location: Paris</li>
            </ul>
        </body>
    </html>
    """

@app.get("/medals")
def get_medals(country: Optional[str] = Query(None)):
    country_list = country.split(',') if country else []
    results = get_medal_summary(noc_codes=country_list)
    return JSONResponse(content=results)
