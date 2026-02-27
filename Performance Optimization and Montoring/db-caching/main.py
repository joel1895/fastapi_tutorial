import sqlite3
import redis
import json
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

#establish database connection
def get_db_connection():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn

#Setup database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor() #need cursor object to run any sql command
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users_table (
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   age INTEGER
                   )
""")
    cursor.execute("INSERT INTO users_table (id, name, age) VALUES (1, 'Micheal', 45)")
    cursor.execute("INSERT INTO users_table (id, name, age) VALUES (2, 'Jim', 35)")
    cursor.execute("INSERT INTO users_table (id, name, age) VALUES (3, 'Pam', 27)")
    conn.commit()
    conn.close()

init_db()

class UserQuery(BaseModel):
    user_id: int

def make_cache_key(user_id: int):
    raw = f"user:{user_id}"
    return hashlib.sha256(raw.encode()).hexdigest()
    
@app.post("/get-user")
def get_user(query: UserQuery):
    cache_key = make_cache_key(query.user_id)

    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Serving from redis Cache!")
        return json.loads(cached_data)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_table WHERE id = ?", (query.user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"message": "User not found."}
    
    result = {'id': row['id'], "name": row['name'], 'age': row['age']}
    redis_client.set(cache_key, ex=3600, value=json.dumps(result))
    print("Fetched from DB and Cached!")

    return result
