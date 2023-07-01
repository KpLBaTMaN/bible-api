
import sqlite3
import random
import pandas as pd
from fastapi import HTTPException

database_file = 'database.db'


def populate_database():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS verses (id INTEGER PRIMARY KEY AUTOINCREMENT, chapter INTEGER, verse INTEGER, text TEXT, translation_id TEXT, book_id TEXT, book_name TEXT)')
    
    # populate database 
    csv_path = "./data/kjv.csv"
    df = pd.read_csv(csv_path)

    # Insert the verses into the database
    for verse in df.to_dict('records'):
        cursor.execute('INSERT INTO verses (chapter, verse, text, translation_id, book_id, book_name) VALUES (?, ?, ?, ?, ?, ?)',
                   (verse["chapter"], verse["verse"], verse["text"], verse["translation_id"], verse["book_id"], verse["book_name"]))
        
    conn.commit()
    conn.close()
    



def get_random_verse():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    # Retrieve the total count of verses in the table
    cursor.execute("SELECT COUNT(*) FROM verses")
    total_verses = cursor.fetchone()[0]

    # Generate a random verse ID
    random_verse_id = random.randint(1, total_verses)

    # Fetch the random verse from the database
    cursor.execute("SELECT chapter, verse, text, translation_id, book_id, book_name FROM verses WHERE id = ?", (random_verse_id,))
    verse_data = cursor.fetchone()

    # Create a dictionary with the verse data
    verse = {
        "chapter": verse_data[0],
        "verse": verse_data[1],
        "text": verse_data[2],
        "translation_id": verse_data[3],
        "book_id": verse_data[4],
        "book_name": verse_data[5]
    }
    conn.commit()
    conn.close()
    return verse

def search_verses(keyword: str):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    # Execute the SQL query to search for verses based on the keyword
    cursor.execute("SELECT chapter, verse, text, translation_id, book_id, book_name FROM verses WHERE text LIKE ?", ('%' + keyword + '%',))
    verse_data = cursor.fetchall()

    # Create a list of dictionaries with the verse data
    verses = []
    for verse in verse_data:
        verse_dict = {
            "chapter": verse[0],
            "verse": verse[1],
            "text": verse[2],
            "translation_id": verse[3],
            "book_id": verse[4],
            "book_name": verse[5]
        }
        verses.append(verse_dict)

    conn.commit()
    conn.close()
    return verses


def create_verse(verse: dict):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO verses (chapter, verse, text, translation_id, book_id, book_name) VALUES (?, ?, ?, ?, ?, ?)',
                   (verse["chapter"], verse["verse"], verse["text"], verse["translation_id"], verse["book_id"], verse["book_name"]))
    conn.commit()
    conn.close()
    return {"message": "Verse created"}


def retrieve_verse(book: str, chapter: int, verse: int):
    # Retrieve a specific verse by reference
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT text, translation_id, book_id, book_name "
            "FROM verses WHERE book_name = ? AND chapter = ? AND verse = ?",
            (book, chapter, verse)
        )
        verse_data = cursor.fetchone()

    # Check if the verse exists in the database
    if verse_data is None:
        raise HTTPException(status_code=404, detail="Verse not found")

    # Create a dictionary with the verse data
    verse = {
        "text": verse_data[0],
        "translation_id": verse_data[1],
        "book_id": verse_data[2],
        "book_name": verse_data[3]
    }

    return verse


def retrieve_verses(book: str, chapter: int):
    # Establish a connection to the database
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()

        # Execute the SQL query to retrieve all verses in the chapter
        cursor.execute("SELECT text, translation_id, book_id, book_name, verse FROM verses WHERE book_name = ? AND chapter = ?", (book, chapter))
        verses_data = cursor.fetchall()

        # Check if any verses exist in the chapter
        if not verses_data:
            raise HTTPException(status_code=404, detail="No verses found in the chapter")

        # Create a list of verse dictionaries
        verses = []
        for verse_data in verses_data:
            verse = {
                "text": verse_data[0],
                "translation_id": verse_data[1],
                "book_id": verse_data[2],
                "book_name": verse_data[3],
                "verse": verse_data[4]
            }
            verses.append(verse)

        return verses
    


def retrieve_book(book: str):
    # Establish a connection to the database
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()

        # Execute the SQL query to retrieve all verses in the book
        cursor.execute(
            "SELECT text, translation_id, book_id, book_name, chapter, verse "
            "FROM verses WHERE book_name = ?",
            (book,)
        )
        verses_data = cursor.fetchall()

        # Check if any verses exist in the book
        if not verses_data:
            raise HTTPException(status_code=404, detail="No verses found in the book")

        # Create a list of verse dictionaries
        verses = []
        for verse_data in verses_data:
            verse = {
                "text": verse_data[0],
                "translation_id": verse_data[1],
                "book_id": verse_data[2],
                "book_name": verse_data[3],
                "chapter": verse_data[4],
                "verse": verse_data[5]
            }
            verses.append(verse)

        return verses

# def get_verse(verse_id: int):
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM verses WHERE id = ?', (verse_id,))
#     verse = cursor.fetchone()
#     conn.close()
#     return {"verse": verse}