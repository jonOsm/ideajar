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
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# --- Include Routers ---
app.include_router(system.router, prefix="/api")
app.include_router(pitches.router, prefix="/api")

# --- Auth Routers ---
from app.users import auth_backend, fastapi_users
from app.models import UserRead, UserCreate, UserUpdate

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/users",
    tags=["users"],
)


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