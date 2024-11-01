from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models.omdb_movie import (
    Movie,
    MovieCreateIn,
    MoviePublicOut,
    MoviesPublicOut,
    MovieUpdateIn,
)

from app.models.user import Message
from app.crud.movies import read_movies_by_ids

router = APIRouter()

@router.get("/", response_model=MoviesPublicOut)
def read_movies(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve Movies
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Movie)
        count = session.exec(count_statement).one()
        statement = select(Movie).offset(skip).limit(limit)
        movies = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Movie)
            .where(Movie.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Movie)
            .where(Movie.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )

        movies = session.exec(statement).all()

    return MoviesPublicOut(data=movies, count=count)


@router.get("/liked", response_model=MoviesPublicOut)
def read_liked_movies(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Get Movies by IDs
    """
    movies = read_movies_by_ids(session, current_user)

    return movies


@router.get("/{id}", response_model=MoviePublicOut)
def read_movie(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get Movie by ID.
    """
    movie = session.get(Movie, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie Not found")
    if not current_user.is_superuser and (movie.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return movie


@router.post("/", response_model=MoviePublicOut)
def create_movie(
    *, session: SessionDep, current_user: CurrentUser, movie_in: MovieCreateIn
) -> Any:
    """
    Create new Movie.
    """
    movie = Movie.model_validate(movie_in, update={"owner_id": current_user.id})
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

@router.put("/{id}", response_model=MoviePublicOut)
def update_movie(
    *, session: SessionDep, current_user: CurrentUser, id: int, movie_in: MovieUpdateIn
) -> Any:
    """
    Update an Movie.
    """
    movie = session.get(Movie, id)
    if not movie:
        raise HTTPException(status_code=444, detail="Movie not found")
    if not current_user.is_superuser and (movie.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = movie_in.model_dump(exclude_unset=True)
    movie.sqlmodel_update(update_dict)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

@router.delete("/{id}")
def delete_movie(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete an Movie.
    """
    movie = session.get(Movie, id)
    if not movie:
        raise HTTPException(status_code=444, detail="Movie not found")
    if not current_user.is_superuser and (movie.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(movie)
    session.commit()
    return Message(message="Movie deleted successfully")