from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.utils import get_olympic_data

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

@app.get("/olympics")
def get_olympics_data():
    data = get_olympic_data()
    return {"data": data}
