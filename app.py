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
    get_verses,
    create_verse
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


@app.post("/verses")
async def create_verse_endpoint(verse: dict):
    return create_verse(verse)

@app.get("/verses/{verse_id}")
async def get_verse_endpoint(verse_id: int):
    return get_verse(verse_id)



# Run the FastAPI application using uvicorn
if __name__ == "__main__":
    # Automatically open the application in the browser
    webbrowser.open("http://localhost:8000")

    uvicorn.run(app, host="localhost", port=8000)