from __future__ import annotations

from datetime import datetime
from typing import Optional, TypedDict
from uuid import uuid1

from flask import session
from flask_login import UserMixin
from flask_sqlalchemy.model import DefaultMeta
from flaskapp.database import db
from flaskapp.models.helpers import now_local_time
from sqlalchemy import Boolean, Column, DateTime, Integer, String

# Always use self for the first argument to instance methods.
# Always use cls for the first argument to class methods.
# class User(UserMixin):
#     def __init__(self, user_id: str, name: str):
#         self.id = user_id
#         self.name = name
#         user_entry = {
#             "id": self.id,
#             "name": self.name,
#         }
#         # Create session user db if not already exists
#         user_db = session.get("user_db")
#         if not user_db:
#             session["user_db"] = {}
#         # Add user to db if user ID does not yet exist
#         if self.id not in session["user_db"]:
#             session["user_db"].update({self.id: user_entry})
#     def is_authenticated(self):
#         if "user_db" not in session:
#             return False
#         # User authenticated if their ID exists in the user_db dict
#         return True if self.id in session["user_db"] else False
#     # Get user object if exists, None otherwise
#     @classmethod
#     def get(cls, user_id: str):
#         if "user_db" in session:
#             if user_id in session["user_db"]:
#                 user = session["user_db"].get(user_id)
#                 return User(
#                     user_id=user["id"],
#                     name=user["name"],
#                 )
#     # Clear current user entry from user db
#     @classmethod
#     def clear(cls, user_id: str):
#         if "user_db" in session:
#             if user_id in session["user_db"]:
#                 session["user_db"].pop(user_id)

BaseModel: DefaultMeta = db.Model  # type: ignore


class UserModel(TypedDict):
    user_id: int
    unique_id: str
    username: str
    display_name: Optional[str]
    password: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String(100), nullable=False, default=str(uuid1()))
    username = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=True)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=now_local_time)
    updated_at = Column(DateTime, default=now_local_time, onupdate=now_local_time)

    def __init__(
        self, *, username=None, display_name=None, password=None, is_admin=False
    ) -> None:
        """* keyword arguments"""
        self.username = username
        self.display_name = display_name
        self.password = password
        self.is_admin = is_admin

    def get_id(self) -> str:
        """
        This column to  user as ID. UUID4 is better
        """
        return str(self.user_id)

    def to_json(self):
        return {"username": self.username}

    def to_dict(self) -> UserModel:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # type: ignore

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username}, unique_id={self.unique_id}, is_admin={self.is_admin} ...)"

    def save(self):
        # inject self into db session
        db.session.add(self)
        # commit change and save the object
        db.session.commit()
        return self

    @classmethod
    def get_all(cls) -> list[User]:
        return db.session.execute(db.select(cls)).scalars().all()  # type: ignore

    @classmethod
    def get_admins(cls) -> list[User]:
        stmt = db.select(cls).where(User.is_admin.is_(False))  # type: ignore
        return db.session.execute(stmt).scalars().all()  # type: ignore
