from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import health
from app.routers import place

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="LocalHub 지역 정보 공유 커뮤니티 API",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health.router,
    prefix="/api",
)

app.include_router(
    place.router
)

@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "LocalHub API",
        "docs": "/docs",
    }