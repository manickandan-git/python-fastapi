from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth,vote
import os,sys

from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)

#main file

app = FastAPI()


def get_port(default: int = 10000) -> int:
    """
    Read the port from the PORT environment variable, fallback to `default`.
    Ensures the returned value is an integer in the valid TCP port range.
    """
    raw = os.getenv("PORT", str(default))
    try:
        port = int(raw)
    except ValueError:
        return default

    if not (1 <= port <= 65535):
        return default

    return port

if __name__ == "__main__":
    port = get_port(10000)
    host = "0.0.0.0"  # Listen on all interfaces, like Express/Node default
 
    # For development use Flask's built-in server. For production, run via gunicorn/uvicorn.
    try:
        app.run(host=host, port=port)
    except OSError as e:
        sys.exit(1)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}





    



    
    