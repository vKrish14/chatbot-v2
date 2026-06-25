import logging
from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    description="Production-ready Chatbot V2 API"
)

# Include API routes
from app.api.chat import router as chat_router
from app.api.upload import router as upload_router
from app.api.diagnostics import router as diagnostics_router
from app.api.routes import router as core_router # keep memory/improve stuff

app.include_router(chat_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(diagnostics_router, prefix="/api")
app.include_router(core_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.app_name} in {settings.environment} mode.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=settings.port, 
        reload=(settings.environment == "development")
    )
