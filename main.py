from fastapi import FastAPI
from ddd.application.user.use_cases import user_routes

app = FastAPI()
app.include_router(user_routes)

@app.get("/")
async def root():
    return "Template Microserivicio"