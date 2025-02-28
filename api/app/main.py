from fastapi import FastAPI

app = FastAPI(title="Chipmunks")


@app.get("/")
def hello():
    """Hello, Chipmunks!"""
    return {"message": "Hello, Chipmunks!"}
