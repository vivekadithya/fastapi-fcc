from sqlalchemy import func
from ..oauth2 import get_current_user
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from .. import models
from ..schemas import PostCreate, Post, PostOut
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Get all posts
@router.get("/", response_model=List[PostOut])
async def get_posts(db: Session=Depends(get_db), limit: int=10, skip: int=0, search: Optional[str]=""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# Get post created by the current user
@router.get("/current_user", status_code=status.HTTP_200_OK, response_model=List[PostOut]) 
def get_current_user_posts(db: Session=Depends(get_db), current_user: int=Depends(get_current_user), limit: int=10, skip: int=0, search: Optional[str]=""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts to display")
    return posts

# Create a Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session=Depends(get_db), current_user: int=Depends(get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) # The ** takes care of extracting the properties and assigning them to the Columns

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# Retrieving a single post
@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session=Depends(get_db)): 
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'post with id: {id} was not found!')

    return post

# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(get_current_user) ):

    post = db.query(models.Post).filter(models.Post.id==id)
    
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} not found.")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED, detail= "Not authorized to perform this action.")
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post 
@router.put("/{id}", response_model=Post)
def update_post(id: int, post: PostCreate, db: Session=Depends(get_db), current_user: int=Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id==id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} not found.")
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action.")
    
    post_query.update(post.model_dump())

    db.commit()
    
    return post_query.first()