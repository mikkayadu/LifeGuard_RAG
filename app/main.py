from fastapi import FastAPI
from fastapi.middleware import CORSMiddleware
from app.routes.upload import router as upload_router
from app.routes.ask import router as ask_router

app = FastAPI(
    title="Health And Fitness Assistant",
    description="Ask questions about uploaded health PDF reports.",
    version="1.0.0"
)
app.include_router(upload_router, prefix="/api")
app.include_router(ask_router, prefix="/api")
