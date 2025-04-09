# main.py
from fastapi import FastAPI
from database import cursor

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


@app.get("/user")
def read_root2():
    rows = cursor.fetchall()

    return {"message": rows}
