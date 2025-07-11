from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, conint

# ------------------ USER ------------------
class User(BaseModel):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ------------------ POST ------------------
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: ResponseUser

    class Config:
        orm_mode = True

# ------------------ TOKEN ------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

# ------------------ VOTE ------------------
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)  # 0 = remove like, 1 = like

# ------------------ COMMENT ------------------
# class CommentCreate(BaseModel):
#     post_id: int
#     content: str
#
# class CommentResponse(BaseModel):
#     id: int
#     content: str
#     created_at: datetime
#     user: ResponseUser
#
#     class Config:
#         orm_mode = True

# ------------------ POST WITH LIKES + COMMENTS ------------------
# class PostWithVotesAndComments(BaseModel):
#     Post: PostResponse
#     likes: int
#     comments: List[CommentResponse]
#
#     model_config = {"from_attributes": True}
#
# # REMOVE CommentCreate, CommentResponse



# CLEAN PostWithVotesAndComments (remove comments)
class PostWithVotesAndComments(BaseModel):
    Post: PostResponse
    likes: int

    model_config = {"from_attributes": True}  # keep this for clean serialization


