from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func,or_
from .. import models, schemas,oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
async def get_posts( db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip:int = 0, search: Optional[str]=""):
    try:
        '''
        posts=  db.query(models.Post).filter(
           or_(models.Post.title.contains(search),
            models.Post.content.contains(search)
            )).limit(limit).offset(skip).all()
        #return posts
        '''
    
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
                or_(models.Post.title.contains(search),
                models.Post.content.contains(search)
                )).limit(limit).offset(skip).all()
    
        return posts

    except Exception as e:
        return e
        
@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post=  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()   
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    db_post= db.query(models.Post).filter(models.Post.id == id)
    if db_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
    if db_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    db_post.delete(synchronize_session=False)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.PostBase,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    db_post= db.query(models.Post).filter(models.Post.id == id)
    if db_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
    if db_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    db_post.update(post.model_dump(),synchronize_session=False)
    db.commit() 
    return db_post.first()

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post (owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post