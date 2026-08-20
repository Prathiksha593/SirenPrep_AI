import re
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="SirenPrep AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DistressMessage(BaseModel):
    raw_text: str
    source: str = "SMS"

class Incident(BaseModel):
    category: str
    location_text: str
    lat: float
    lng: float
    priority_score: int
    raw_text: str

CATEGORIES = {
    "trapped": ["trapped", "stuck", "roof", "collapsed", "under"],
    "medical": ["injured", "bleeding", "unconscious", "heart", "doctor", "hospital"],
    "fire": ["fire", "smoke", "explosion", "burning"],
    "flood": ["water", "drowning", "flood", "rising", "submerged"]
}

@app.post("/api/analyze", response_model=Incident)
async def analyze_message(msg: DistressMessage):
    text = msg.raw_text.lower()
    
    # Categorization
    category = "General Rescue"
    for cat, keywords in CATEGORIES.items():
        if any(kw in text for kw in keywords):
            category = cat.capitalize()
            break
            
    # Priority Scoring (1 to 10 scale)
    score = 5
    if "trapped" in text or "drowning" in text or "bleeding" in text:
        score += 4
    if "child" in text or "baby" in text or "elderly" in text:
        score += 1
    score = min(score, 10)
    
    # Mock Entity/Location Extraction
    location_text = "Unknown Location"
    match = re.search(r'(?:at|near|in)\s+([A-Za-z0-9\s]+)', msg.raw_text, re.IGNORECASE)
    if match:
        location_text = match.group(1).strip()
        
    return Incident(
        category=category,
        location_text=location_text,
        lat=13.0827,  # Default demo coordinates (Chennai center)
        lng=80.2707,
        priority_score=score,
        raw_text=msg.raw_text
    )

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SirenPrep API"}
