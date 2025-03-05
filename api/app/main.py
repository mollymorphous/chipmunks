import logging

from fastapi import FastAPI

from .config import Config

config = Config()

logging.basicConfig(level=config.log.level)

app = FastAPI(title="Chipmunks", debug=config.debug.stack_traces)


@app.get("/")
def hello():
    """Hello, Chipmunks!"""
    return {"message": "Hello, Chipmunks!"}
