from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.user import User

# 基本属性
class MovieBase(SQLModel):
    title: str
    year: str
    rated: str | None = None
    released: str | None = None
    runtime: str | None = None
    genre: str | None = None
    director: str | None = None
    writer: str | None = None
    actors: str | None = None
    plot: str | None = None
    language: str | None = None
    country: str | None = None
    awards: str | None = None
    poster: str | None = None
    imdb_rating: str | None = None
    imdb_votes: str | None = None
    imdb_id: str
    metascore: str | None = None
    box_office: str | None = None
    production: str | None = None
    website: str | None = None

# 创建电影时所需的属性
class MovieCreateIn(MovieBase):
    title: str
    year: str
    rated: str | None = None
    released: str | None = None
    runtime: str | None = None
    genre: str | None = None
    director: str | None = None
    writer: str | None = None
    actors: str | None = None
    plot: str | None = None
    language: str | None = None
    country: str | None = None
    awards: str | None = None
    poster: str | None = None
    imdb_rating: str | None = None
    imdb_votes: str | None = None
    imdb_id: str
    metascore: str | None = None
    box_office: str | None = None
    production: str | None = None
    website: str | None = None

# 更新电影时所需的属性
class MovieUpdateIn(MovieBase):
    title: str | None = None

# 数据库模型，表名由类名推导
class Movie(MovieBase, table=True):
    __tablename__ = "movie"

    id: Optional[int] = Field(default=None, primary_key=True)
    ratings: str = Field(default="") # ratings store as the str and separate by ','

    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="movies")

# API 返回模型，id 总是必需的
class MoviePublicOut(MovieBase):
    id: int
    owner_id: int

# API 返回的列表模型
class MoviesPublicOut(SQLModel):
    data: list[MoviePublicOut]
    count: int
