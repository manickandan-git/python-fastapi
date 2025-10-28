from fastapi.params import Depends
from typing_extensions import Annotated
from fastapi import FastAPI

from app.models import User
from app.oauth2 import get_current_user
from .routers import post, user, auth,vote

from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)

#main file

app = FastAPI()

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

# 2. Use the dependency on a route
@app.get("/users/me", response_model=User)
async def read_users_me(
    # By including this dependency, FastAPI adds security requirements
    # to the route's definition in the generated OpenAPI spec.
    current_user: Annotated[User, Depends(get_current_user)] 
):
    return current_user





    



    
    