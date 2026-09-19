from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.routers import download, health, resolve

app = FastAPI(
    title="Utooload Backend",
    description="Resolve + download YouTube video/audio for the Utooload app.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(resolve.router, prefix="/api")
app.include_router(download.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Utooload's backend is up!!"}

