
import sqlite3

def create_verse(verse: dict):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO verses (chapter, verse, text, translation_id, book_id, book_name) VALUES (?, ?, ?, ?, ?, ?)',
                   (verse["chapter"], verse["verse"], verse["text"], verse["translation_id"], verse["book_id"], verse["book_name"]))
    conn.commit()
    conn.close()
    return {"message": "Verse created"}


def get_verses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM verses')
    verses = cursor.fetchall()
    conn.close()
    return {"verses": verses}


def get_verse(verse_id: int):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM verses WHERE id = ?', (verse_id,))
    verse = cursor.fetchone()
    conn.close()
    return {"verse": verse}