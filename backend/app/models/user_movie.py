from sqlmodel import Field, ARRAY, Column, Integer
from sqlalchemy.ext.mutable import MutableList

from app.models import SQLModel
from typing import List

# Shared properties
class UserMovieBase(SQLModel):
    # The ARRAY type, when used with the SQLAlchemy ORM, does not detect in-place mutations to the array. 
    # In order to detect these, MutableList is needed
    movies: List[int] = Field(default=[], sa_column=Column(MutableList.as_mutable(ARRAY(Integer))))

class UserMovieCreateIn(UserMovieBase):
    movies: List[int] = Field(default=[], sa_column=Column(MutableList.as_mutable(ARRAY(Integer))))

class UserMovieUpdateIn(UserMovieBase):
    movies: List[int] = Field(default=[], sa_column=Column(MutableList.as_mutable(ARRAY(Integer))))

class UserMovie(UserMovieBase, table=True):
    __tablename__ = "usermovie"

    owner_id: int | None= Field(default=None, primary_key=True,
                                 foreign_key="user.id",
                                 nullable=False)

class UserMoviePublicOut(UserMovieBase):
    owner_id: int
