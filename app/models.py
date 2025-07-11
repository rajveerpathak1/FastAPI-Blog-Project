from sqlalchemy import Column, Integer, String, Boolean, text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(1000), nullable=False)
    published = Column(Boolean,nullable=False, server_default=text("TRUE"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="posts")
    votes = relationship("VoteTable", back_populates="post")

    # comments = relationship("Comment", back_populates="post")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    posts = relationship("Post", back_populates="owner")
    votes = relationship("VoteTable", back_populates="user")

    # comments = relationship("Comment", back_populates="user", cascade="all, delete")


class VoteTable(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")


# class Comment(Base):
#     __tablename__ = "comments"
#
#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
#
#     user = relationship("User", back_populates="comments")
#     post = relationship("Post", back_populates="comments")




