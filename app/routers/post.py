from collections import defaultdict
from typing import List,Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# ----------------- GET ALL POSTS -----------------
@router.get("/", response_model=List[schemas.PostWithVotesAndComments])
def read_posts(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    posts_with_likes = (
        db.query(models.Post, func.count(models.VoteTable.post_id).label("likes"))
        .join(models.VoteTable, models.VoteTable.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        {
            "Post": post,
            "likes": likes
        }
        for post, likes in posts_with_likes
    ]

# ----------------- GET SINGLE POST BY ID -----------------
@router.get("/{id}", response_model=schemas.PostWithVotesAndComments)
def read_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    post_with_likes = (
        db.query(models.Post, func.count(models.VoteTable.post_id).label("likes"))
        .join(models.VoteTable, models.VoteTable.post_id == models.Post.id, isouter=True)
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )

    if not post_with_likes:
        raise HTTPException(status_code=404, detail="Post not found")

    post, likes = post_with_likes
    return {
        "Post": post,
        "likes": likes
    }

# ----------------- CREATE A POST -----------------
@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    # post_data = post.dict()
    # post_data["owner_id"] = current_user.id
    db_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# ----------------- UPDATE A POST -----------------
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
        id: int,
        post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")

    #  Authorization check (corrected)
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post"
        )

    for key, value in post.dict().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post

# ----------------- DELETE A POST -----------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")

    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post"
        )

    db.delete(db_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
