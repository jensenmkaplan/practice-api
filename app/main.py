from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Practice API", version="0.1.0")


class EchoRequest(BaseModel):
    message: str


class HelloRequest(BaseModel):
    text: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to Practice API"}


@app.post("/echo")
def echo(payload: EchoRequest) -> dict[str, str]:
    return {"echo": payload.message}


@app.post("/hello")
def hello(payload: HelloRequest) -> dict[str, str]:
    return {"result": f"{payload.text} world"}

