from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload import router as upload_router
from app.routes.ask import router as ask_router

app = FastAPI(
    title="Health And Fitness Assistant",
    description="Ask questions about uploaded health PDF reports.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router, prefix="/api")
app.include_router(ask_router, prefix="/api")
