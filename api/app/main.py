import logging

from fastapi import FastAPI

from .config import Config

# Set up app instance
config = Config()
logging.config.dictConfig(config.logging.config_dict())
app = FastAPI(
    title="Chipmunks", debug=config.debug.stack_traces, version=config.build.version
)


@app.get("/")
def hello():
    """Hello, Chipmunks!"""
    return {"message": "Hello, Chipmunks!"}
