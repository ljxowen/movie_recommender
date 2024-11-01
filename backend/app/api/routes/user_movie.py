from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models.user_movie import (
    UserMovie,
    UserMovieCreateIn,
    UserMovieUpdateIn,
    UserMoviePublicOut,
)
from app.models.user import Message
from app.crud.user_movie import add_userMovie, remove_userMovie


router = APIRouter()

@router.get("/", response_model=UserMoviePublicOut)
def read_user_movie(
    session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Retrieve User Movie
    """
    statement = (
        select(UserMovie.movies)
        .where(UserMovie.owner_id == current_user.id)
    )

    movies = session.exec(statement).all()
    if not movies:
        raise HTTPException(status_code=404, detail="UserMovie not found")

    return UserMoviePublicOut(movies=movies[0], owner_id=current_user.id)


@router.post("/", response_model=UserMoviePublicOut)
def create_user_movie(
    *, session: SessionDep, current_user: CurrentUser, user_movie_in: UserMovieCreateIn
) -> Any:
    """
    Create new User Movie
    """
    user_movie = UserMovie.model_validate(user_movie_in, update={"owner_id": current_user.id})
    session.add(user_movie)
    session.commit()
    session.refresh(user_movie)
    return user_movie


@router.put("/", response_model=UserMoviePublicOut)
def update_user_movie(
    *, session: SessionDep, current_user: CurrentUser, user_movie_in: UserMovieUpdateIn
) -> Any:
    """
    Update an User Movie
    """
    user_movie = session.get(UserMovie, current_user.id)
    if not user_movie:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_movies = user_movie_in.model_dump(exclude_unset=True) 
    user_movie.sqlmodel_update(update_movies) 
    session.add(user_movie) 
    session.commit() 
    session.refresh(user_movie) 
    
    return user_movie


@router.put("/add/{id}", response_model=UserMoviePublicOut)
def add_user_movie(
    *, session: SessionDep, current_user: CurrentUser, id: int
) -> Any:
    """
    Add movie id to UserMovie
    """
    user_movie = add_userMovie(session=session, current_user=current_user, movie_id=id)
    if not user_movie:
        raise HTTPException(status_code=404, detail="UserMovie not found")
    
    return user_movie


@router.put("/remove/{id}", response_model=UserMoviePublicOut)
def remove_user_movie(
    *, session: SessionDep, current_user: CurrentUser, id: int
) -> Any:
    """
    Remove movie id to UserMovie
    """
    user_movie = remove_userMovie(session=session, current_user=current_user, movie_id=id)
    if not user_movie:
        raise HTTPException(status_code=404, detail="UserMovie not found")
    
    return user_movie


@router.delete("/{id}")
def delete_user_movie(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete an User Movie
    """
    user_movie = session.get(UserMovie, id)
    if not user_movie:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(user_movie)
    session.commit
    return Message(message="Item deleted successfully")
