from ..oauth2 import get_current_user
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from .. import models
from ..schemas import Vote


router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session=Depends(get_db), current_user: int=Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote ({vote.post_id}) not found.")

    vote_present = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id).first()

    if vote.dir == 1:
        # Vote Up
        if vote_present:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User ({current_user.id}) has already up voted this post.")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)

        return new_vote

    else:
        # Vote Down
        if not vote_present:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User ({current_user.id}) is yet to up vote this post!")
        
        down_vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)

        down_vote_query.delete()
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)