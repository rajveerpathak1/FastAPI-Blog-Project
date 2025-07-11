from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    vote_query = db.query(models.VoteTable).filter(
        models.VoteTable.post_id == vote.post_id,
        models.VoteTable.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=409, detail="You have already liked this post")
        new_vote = models.VoteTable(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Liked the post"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="You haven't liked this post yet")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Unliked the post"}
