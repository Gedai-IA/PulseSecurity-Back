from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.routes import publications, dashboard, analysis, auth, object_detector

app = FastAPI(
    title="Scrapping Backend API",
    description="API para análise de sentimento e tópicos em publicações",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["auth"])
app.include_router(publications.router, prefix=settings.API_V1_PREFIX, tags=["publications"])
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX, tags=["dashboard"])
app.include_router(analysis.router, prefix=settings.API_V1_PREFIX, tags=["analysis"])
app.include_router(object_detector.router, prefix=settings.API_V1_PREFIX, tags=["object-detector"])


@app.get("/")
async def root():
    return {"message": "Scrapping Backend API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

