from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pathlib import Path
# ADD THESE 3 LINES
import sys
sys.path.append(str(Path(__file__).parent.parent / "ml_engines"))  # <-- allows import
from engine import generate_response  # <-- uncensored replies



app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# SQLite setup
conn = sqlite3.connect('amora.db')
conn.execute('CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, message TEXT, sender TEXT, chat_id TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS characters (id INTEGER PRIMARY KEY, name TEXT, icon_path TEXT)')

@app.post("/send_message")
async def send_message(message: str, sender: str, chat_id: str):
    # Save user message
    conn.execute('INSERT INTO chats (message, sender, chat_id) VALUES (?, ?, ?)', (message, sender, chat_id))
    
    # Generate AI replies from 8 characters
    characters = ["Luna", "Mia", "Zoe", "Kara", "Sasha", "Roxy", "Vixen", "Jade"]
    for char in characters:
        ai_reply = generate_response(message, char)
        conn.execute('INSERT INTO chats (message, sender, chat_id) VALUES (?, ?, ?)', (ai_reply, char, chat_id))
    
    conn.commit()
    return {"status": "sent"}

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    path = Path("uploads") / file.filename
    path.parent.mkdir(exist_ok=True)
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"url": str(path)}

@app.get("/get_chats/{chat_id}")
async def get_chats(chat_id: str):
    cursor = conn.execute('SELECT * FROM chats WHERE chat_id = ?', (chat_id,))
    return [{"message": row[1], "sender": row[2]} for row in cursor.fetchall()]

# Add endpoints for characters: create, list, etc.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
