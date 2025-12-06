import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# --- 1. Define API Routes (Add operation_id for clean types) ---
from typing import List, Optional, Literal
from uuid import UUID, uuid4
from pydantic import BaseModel

# --- Models ---
class Pitch(BaseModel):
    id: UUID
    title: str
    description: str
    type: Literal["idea", "opinion", "pitch"]
    submitter: str = "Anonymous"

class Vote(BaseModel):
    pitch_id: UUID
    vote_type: Literal["like", "dislike"]

# --- In-Memory Store ---
PITCHES: List[Pitch] = [
    Pitch(id=uuid4(), title="Cat Café & Laundromat", description="Drink coffee and pet cats while waiting for your laundry.", type="idea", submitter="Alice"),
    Pitch(id=uuid4(), title="Pineapple on Pizza is Good", description="The sweetness cuts the saltiness. Ideally with jalapeños.", type="opinion", submitter="Bob"),
    Pitch(id=uuid4(), title="Uber for Dog Walking", description="On-demand dog walkers nearby. GPS tracked.", type="pitch", submitter="Charlie"),
]

VOTES: List[Vote] = []

# --- 1. Define API Routes (Add operation_id for clean types) ---
@app.get("/api/health", operation_id="health_check", tags=["System"])
def health():
    return {"status": "ok", "environment": os.getenv("ENV", "dev")}

@app.get("/api/pitches", response_model=List[Pitch], operation_id="get_pitches", tags=["Pitches"])
def get_pitches() -> List[Pitch]:
    """Get a list of pitches to swipe on."""
    return PITCHES

@app.post("/api/vote", operation_id="submit_vote", tags=["Pitches"])
def submit_vote(vote: Vote):
    """Submit a swipe vote."""
    VOTES.append(vote)
    return {"status": "recorded", "vote": vote}

# --- 2. Static Assets (Production Only) ---
# We check if the folder exists so this doesn't crash in local dev
if os.path.exists("/app/frontend/dist"):
    app.mount("/assets", StaticFiles(directory="/app/frontend/dist/assets"), name="assets")

# --- 3. SPA Fallback (Production Only) ---
@app.get("/{full_path:path}")
async def serve_vue_app(full_path: str):
    # If API request falls through, return 404 (don't serve index.html)
    if full_path.startswith("api"):
        return {"error": "Not Found"}, 404
    
    # In production, serve the Vue app
    if os.path.exists("/app/frontend/dist/index.html"):
        return FileResponse("/app/frontend/dist/index.html")
    
    # In local dev, just return a message
    return {"message": "Run 'npm run dev' to see the frontend"}