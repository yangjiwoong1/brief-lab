# app/main.py
from fastapi import FastAPI
from src.app.router import router

app = FastAPI()
app.include_router(router)
