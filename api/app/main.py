import logging

from fastapi import FastAPI

from .settings import Settings

# Set up app instance
settings = Settings()
logging.basicConfig(level=settings.log.level, format=settings.log.format, style="{")
app = FastAPI(
    title="Chipmunks", debug=settings.debug.stack_traces, version=settings.build.version
)


@app.get("/")
def hello():
    """Hello, Chipmunks!"""
    return {"message": "Hello, Chipmunks!"}
