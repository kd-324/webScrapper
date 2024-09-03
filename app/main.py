import uvicorn
from fastapi import FastAPI
from app.api.v1.endpoints import scrapper

app = FastAPI()

app.include_router(scrapper.router)
uvicorn.run(app, host="127.0.0.1", port=8000)