import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .db import init_db, engine
from .api.routers import pitches, system

# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Retrieve/Check connection on startup
    # We could also create tables here if not using Alembic: await init_db()
    yield
    # Clean up DB connections on shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# --- Include Routers ---
app.include_router(system.router, prefix="/api")
app.include_router(pitches.router, prefix="/api")

# --- Static Assets (Production Only) ---
if os.path.exists("/app/frontend/dist"):
    app.mount("/assets", StaticFiles(directory="/app/frontend/dist/assets"), name="assets")

# --- SPA Fallback (Production Only) ---
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_vue_app(full_path: str):
    if full_path.startswith("api"):
        return {"error": "Not Found"}, 404
    
    if os.path.exists("/app/frontend/dist/index.html"):
        return FileResponse("/app/frontend/dist/index.html")
    
    return {"message": "Run 'npm run dev' to see the frontend"}