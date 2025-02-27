from fastapi import FastAPI

api = FastAPI(title="Chipmunks")


@api.get("/")
def hello():
    """Hello, Chipmunks!"""
    return {"message": "Hello, Chipmunks!"}
