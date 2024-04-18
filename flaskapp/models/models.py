from __future__ import annotations

from datetime import datetime
from typing import Optional, TypedDict
from uuid import uuid4

from flask_login import UserMixin
from flask_sqlalchemy.model import DefaultMeta
from flaskapp.database import db
from flaskapp.models.helpers import utc_now
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Computed, FetchedValue

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
    __table_args__ = (
        db.Index("ix_username", "username"),
        # db.Index("fk_user_othertable", "id"),
    )

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    # extras
    unique_id: Mapped[str] = mapped_column(
        String(100), nullable=False, default=str(uuid4())
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[str] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[str] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)
    # fk_id: Mapped[int] = mapped_column(
    #     Integer, ForeignKey("table.fk_id"), nullable=False, index=True
    # )
    # computed_col: Mapped[int] = mapped_column(
    #     Integer, Computed("substr( username, 1, 4 )", False)
    # )

    def __init__(
        self, *, username, password, display_name=None, is_admin=False
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
        return {
            c.key: getattr(self, c.key) for c in self.__table__.columns  # type: ignore
        }

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
