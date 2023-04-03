from fastapi import FastAPI
from src.presentation.user_api import user_routes
from src.infrastructure.database import Base, engine

app = FastAPI()
app.include_router(user_routes)

@app.get("/")
async def root():
    return "Template Microserivicio"