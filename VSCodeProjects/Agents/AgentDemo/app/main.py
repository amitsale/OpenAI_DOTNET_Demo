# main.py
# Entry point for your FastAPI application

from fastapi import FastAPI
from app.controller import stock_controller

app = FastAPI()

app.include_router(stock_controller.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"greeting": f"Hello, {name}!"}