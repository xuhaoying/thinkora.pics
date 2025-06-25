#!/usr/bin/env python3
import json
import sqlite3
import os

# --- Configuration ---
METADATA_FILE = 'metadata_r2.json'
DB_FILE = 'thinkora.db'
TABLE_NAME = 'images'

def create_database_schema(cursor):
    """
    Defines and creates the database table schema.
    """
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        author_name TEXT,
        author_url TEXT,
        width INTEGER,
        height INTEGER,
        aspect_ratio TEXT,
        url_thumbnail TEXT,
        url_regular TEXT,
        url_download TEXT,
        tags TEXT, -- Stored as a JSON string
        category TEXT,
        quality_score INTEGER,
        file_size TEXT,
        transparent_ratio REAL,
        created_at TEXT,
        unsplash_id TEXT,
        unsplash_url TEXT,
        unsplash_download_location TEXT
    )
    ''')
    print(f"✅ Table '{TABLE_NAME}' schema created or already exists.")

def migrate_json_to_sqlite():
    """
    Reads data from the JSON file and inserts it into the SQLite database.
    """
    print("🚀 Starting migration from JSON to SQLite...")

    # Check for metadata file
    if not os.path.exists(METADATA_FILE):
        print(f"❌ Error: Metadata file not found at '{METADATA_FILE}'. Cannot migrate.")
        return

    # Remove old DB if it exists to ensure a fresh start
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"🗑️ Removed existing database file '{DB_FILE}'.")

    # Connect to SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table
    create_database_schema(cursor)

    # Load JSON data
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        images_data = json.load(f)
    
    print(f"📄 Found {len(images_data)} records in '{METADATA_FILE}'.")

    # Prepare data for insertion
    records_to_insert = []
    for image in images_data:
        # --- Robust field extraction ---
        author_name, author_url = ('Unknown', '#')
        if isinstance(image.get('author'), dict):
            author_name = image['author'].get('name', 'Unknown')
            author_url = image['author'].get('url', '#')
        elif isinstance(image.get('author'), str):
            author_name = image['author']

        width, height, aspect_ratio = (None, None, None)
        if isinstance(image.get('dimensions'), dict):
            width = image['dimensions'].get('width')
            height = image['dimensions'].get('height')
            aspect_ratio = image['dimensions'].get('ratio')

        url_thumbnail, url_regular, url_download = (None, None, None)
        if isinstance(image.get('urls'), dict):
            url_thumbnail = image['urls'].get('thumbnail')
            url_regular = image['urls'].get('regular')
            url_download = image['urls'].get('download')
            
        unsplash_id, unsplash_url, unsplash_download_location = (None, None, None)
        if isinstance(image.get('unsplash'), dict):
            unsplash_id = image['unsplash'].get('id')
            unsplash_url = image['unsplash'].get('url')
            unsplash_download_location = image['unsplash'].get('download_location')

        record = (
            image.get('id'),
            image.get('title'),
            image.get('description'),
            author_name,
            author_url,
            width,
            height,
            aspect_ratio,
            url_thumbnail,
            url_regular,
            url_download,
            json.dumps(image.get('tags', [])), # Convert list of tags to JSON string
            image.get('category'),
            image.get('quality_score'),
            image.get('file_size'),
            image.get('transparent_ratio'),
            image.get('created_at'),
            unsplash_id,
            unsplash_url,
            unsplash_download_location
        )
        records_to_insert.append(record)

    # Insert data into the database
    try:
        cursor.executemany(f'''
        INSERT INTO {TABLE_NAME} (
            id, title, description, author_name, author_url, width, height, 
            aspect_ratio, url_thumbnail, url_regular, url_download, tags, 
            category, quality_score, file_size, transparent_ratio, 
            created_at, unsplash_id, unsplash_url, unsplash_download_location
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', records_to_insert)
        
        # Commit the changes and close the connection
        conn.commit()
        print(f"✅ Successfully inserted {len(records_to_insert)} records into '{DB_FILE}'.")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()
        print("🛑 Database connection closed.")


if __name__ == '__main__':
    migrate_json_to_sqlite() 