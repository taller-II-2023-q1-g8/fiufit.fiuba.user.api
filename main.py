from fastapi import FastAPI
from src.presentation.user_api import user_routes

"""
Application Entry Point
"""

app = FastAPI()
app.include_router(user_routes)

@app.get("/healthcheck")
async def root():
    """Healthcheck endpoint"""
    return "Users Microservice is up and running"
