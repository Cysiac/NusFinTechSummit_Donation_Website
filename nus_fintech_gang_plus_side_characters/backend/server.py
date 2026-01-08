import sqlite3
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Initialize the App
app = FastAPI()

# FIXED: CORSMiddleware setup - removed extra text and properly defined origins
origins = [
    "http://localhost:3000",  # React default port
    "http://127.0.0.1:3000",  # Alternative localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define the Data Model
class DonationRecord(BaseModel):
    amount: float
    sender: str
    tx_hash: str

# 3. Database Setup (SQLite)
def init_db():
    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            sequence INTEGER PRIMARY KEY AUTOINCREMENT, 
            amount REAL, 
            sender TEXT, 
            tx_hash TEXT, 
            status TEXT DEFAULT 'PENDING'
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "TrustBridge Listener is Running"}

@app.post("/register_donation")
def register_donation(record: DonationRecord):
    try:
        with sqlite3.connect('donations.db') as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO donations (amount, sender, tx_hash) VALUES (?, ?, ?)", 
                (record.amount, record.sender, record.tx_hash)
            )
            conn.commit()
            sequence = c.lastrowid
        return {"status": "success", "message": "Donation recorded", "sequence": sequence}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/available_claims")
def get_pending_donations():
    try:
        conn = sqlite3.connect('donations.db')
        c = conn.cursor()
        
        # FIXED: Proper column names and WHERE clause
        c.execute("SELECT sequence, amount, sender, tx_hash FROM donations WHERE status='PENDING'")
        rows = c.fetchall()
        conn.close()
        
        donations_list = []
        for row in rows:
            donations_list.append({
                "sequence": row[0],
                "amount": row[1],
                "sender": row[2],
                "tx_hash": row[3]
            })
            
        return donations_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mark_claimed/{sequence}")
def mark_claimed(sequence: int):
    try:
        with sqlite3.connect('donations.db') as conn:
            c = conn.cursor()
            # FIXED: Check if record exists first
            c.execute("SELECT sequence FROM donations WHERE sequence=?", (sequence,))
            if not c.fetchone():
                raise HTTPException(status_code=404, detail="Donation not found")
                
            c.execute("UPDATE donations SET status='CLAIMED' WHERE sequence=?", (sequence,))
            conn.commit()
        return {"status": "success", "message": f"Donation {sequence} marked as claimed"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mark_refunded/{sequence}")
def mark_refunded(sequence: int):
    try:
        with sqlite3.connect('donations.db') as conn:
            c = conn.cursor()
            # FIXED: Check if record exists first
            c.execute("SELECT sequence FROM donations WHERE sequence=?", (sequence,))
            if not c.fetchone():
                raise HTTPException(status_code=404, detail="Donation not found")
                
            c.execute("UPDATE donations SET status='REFUNDED' WHERE sequence=?", (sequence,))
            conn.commit()
        return {"status": "success", "message": f"Donation {sequence} marked as refunded"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/debug_donation")
async def debug_donation(request: Request):
    try:
        data = await request.json()
        print("Received JSON:", data)
        return {"received": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Additional useful endpoint
@app.get("/all_donations")
def get_all_donations():
    try:
        conn = sqlite3.connect('donations.db')
        c = conn.cursor()
        c.execute("SELECT sequence, amount, sender, tx_hash, status FROM donations ORDER BY sequence DESC")
        rows = c.fetchall()
        conn.close()
        
        donations_list = []
        for row in rows:
            donations_list.append({
                "sequence": row[0],
                "amount": row[1],
                "sender": row[2],
                "tx_hash": row[3],
                "status": row[4]
            })
            
        return donations_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))