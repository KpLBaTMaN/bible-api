import uvicorn
import webbrowser

import sqlite3

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd


from backend.database import (
    get_verse,
    create_verse,
    get_random_verse,
    search_verses
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def populate_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS verses (id INTEGER PRIMARY KEY AUTOINCREMENT, chapter INTEGER, verse INTEGER, text TEXT, translation_id TEXT, book_id TEXT, book_name TEXT)')
    
    # populate database 
    csv_path = "./backend/kjv.csv"
    df = pd.read_csv(csv_path)

    # Insert the verses into the database
    for verse in df.to_dict('records'):
        cursor.execute('INSERT INTO verses (chapter, verse, text, translation_id, book_id, book_name) VALUES (?, ?, ?, ?, ?, ?)',
                   (verse["chapter"], verse["verse"], verse["text"], verse["translation_id"], verse["book_id"], verse["book_name"]))
        
    conn.commit()
    conn.close()
    
populate_database()


@app.get("/v1/verses/random")
def get_random_verse_endpoint():
    # Code to fetch a random Bible verse
    return get_random_verse()
    
@app.get("/v1/verses")
def search_verses_endpoint(keyword: str):
    # Code to search for verses based on a keyword
    return search_verses(keyword)

@app.get("/v1/verses/{book_name}/{chapter}/{verse}")
def get_verse_endpoint(book: str, chapter: int, verse: int):
    # Code to retrieve a specific verse by reference
    return get_verse(book, chapter, verse)

# @app.get("/v1/verses/{book}/{chapter}")
# def get_verses(book: str, chapter: int):
#     # Code to retrieve verses from a specific book and chapter
#     # Return the verses in the desired format
#     return ""

# @app.get("/v1/verses/{book}/{chapter}")
# def get_verses_range(book: str, chapter: int, start: int, end: int):
#     # Code to retrieve a range of verses within a specific book and chapter
#     # Return the verses in the desired format
#     return ""
    

# @app.post("/verses")
# async def create_verse_endpoint(verse: dict):
#     return create_verse(verse)

@app.get("/verses/{verse_id}")
async def get_verse_endpoint(verse_id: int):
    return get_verse(verse_id)


# # Close the database connection when the application shuts down
# @app.on_event("shutdown")
# def close_db_connection():
#     conn.close()


# Run the FastAPI application using uvicorn
if __name__ == "__main__":
    # Automatically open the application in the browser
    webbrowser.open("http://localhost:8000/docs")

    uvicorn.run(app, host="localhost", port=8000)