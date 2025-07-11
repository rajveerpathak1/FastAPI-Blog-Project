# from typing import List
#
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from .. import models, schemas, database, oauth2
#
# router = APIRouter(
#     prefix="/comments",
#     tags=["Comments"]
# )
#
# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentResponse)
# def create_comment(comment: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#
#     new_comment = models.Comment(content=comment.content, user_id=current_user.id, post_id=comment.post_id)
#     db.add(new_comment)
#     db.commit()
#     db.refresh(new_comment)
#     return new_comment
#
# @router.get("/{post_id}", response_model=List[schemas.CommentResponse])
# def get_comments(post_id: int, db: Session = Depends(database.get_db)):
#     comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
#     return comments
