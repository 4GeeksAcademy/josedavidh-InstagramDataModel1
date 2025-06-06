from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, func, Text, Table, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
import enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    #Relationship with other tables, below
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    following_assoc: Mapped[List["Follower"]] = relationship("Follower",
        foreign_keys="[Follower.user_from_id]",
        back_populates="follower")
    followers_assoc: Mapped[List["Follower"]] = relationship("Follower",
        foreign_keys="[Follower.user_to_id]",
        back_populates="followed")

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_post: Mapped[datetime] = mapped_column(DateTime, nullable=False,
        server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    #Relationship
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped["Comment"] = relationship(back_populates="post")
    media: Mapped[List["Media"]] = relationship(back_populates="post")

class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    date_comment: Mapped[datetime] = mapped_column(DateTime, nullable=False,
        server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    
    #Relationship
    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

class Mediatype(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"

class Media(db.Model):
    __tablename__="media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Mediatype] = mapped_column(Enum(Mediatype), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    #Relationship
    post: Mapped["Post"] = relationship(back_populates="media")

class Follower(db.Model):
    __tablename__="follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    #Relationship
    follower: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], back_populates="following_assoc")
    followed: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], back_populates="followers_assoc")