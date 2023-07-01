import uvicorn
import webbrowser

import sqlite3

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd


from backend.database import (
    retrieve_verse,
    retrieve_verses,
    retrieve_book,
    get_random_verse,
    search_verses
)

app = FastAPI(
    title="BibleAPI",
    description="A Bible API that contains the KJV bible. (In development)",
    version="0.0.1",
    contact={
        "name": "Andrew brown",
        "url": "https://github.com/KpLBaTMaN/bible-api"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route for the search page
@app.get('/search', response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


# Route for handling the search request
@app.post('/search/results', response_class=HTMLResponse)
async def search(request: Request, keyword: str = Form(...)):
    verses = search_verses(keyword)  # Call the search_verses function
    return templates.TemplateResponse("results.html", {"request": request, "verses": verses})


@app.get("/v1/verses/random", response_class=JSONResponse)
def get_random_verse_endpoint():
    # Code to fetch a random Bible verse
    return get_random_verse()
    
@app.get("/v1/verses", response_class=JSONResponse)
def search_verses_endpoint(keyword: str):
    # Code to search for verses based on a keyword
    return search_verses(keyword)

@app.get("/v1/verses/{book}/{chapter}/{verse}", response_class=JSONResponse)
def get_verse_endpoint(book: str, chapter: int, verse: int):
    # Code to retrieve a specific verse by reference
    return retrieve_verse(book, chapter, verse)

@app.get("/v1/verses/{book}/{chapter}", response_class=JSONResponse)
def get_verses_endpoint(book: str, chapter: int):
     # Code to retrieve a specific book by reference
    return retrieve_verses(book, chapter)

@app.get("/v1/books/{book}", response_class=JSONResponse)
def get_book(book: str):
    return retrieve_book(book)


# Run the FastAPI application using uvicorn
if __name__ == "__main__":
    domain = "localhost"
    
    # Automatically open the application in the browser
    webbrowser.open(f"http://{domain}:8000/docs")

    uvicorn.run(app, host=domain, port=8000)