from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from app.utils import get_medal_summary, get_top_medals
from starlette.requests import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    top_3_medals = get_top_medals(top=3)
    medal_data = [
        {
            "country": {
                "name": item['country']['name'],
                "code": item['country']['code']
            },
            "medals": item['medals'],
            "total": item['medals']['gold'] + item['medals']['silver'] + item['medals']['bronze']
        }
        for item in top_3_medals['results']
    ]
    return templates.TemplateResponse("index.html", {"request": request, "medal_data": medal_data})


@app.get("/medals")
def get_medals(country: Optional[str] = Query(None)):
    country_list = country.split(',') if country else []
    results = get_medal_summary(noc_codes=country_list)
    return JSONResponse(content=results)

@app.get("/top_medals")
def get_top_medal(top: Optional[int] = Query(3)):
    results = get_top_medals(top=top)
    print(results)
    return JSONResponse(content=results)