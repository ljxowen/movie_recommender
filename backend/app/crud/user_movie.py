from app.models.user_movie import UserMovie

from app.api.deps import SessionDep, CurrentUser

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_userMovie(*, session: SessionDep, current_user: CurrentUser, movie_id: int) -> UserMovie:
    """
    Add a movie id to movies in usermovie table
    """
    user_movie = session.get(UserMovie, current_user.id)
    if not user_movie:
        raise ValueError(f"UserMovie with User ID {current_user.id} not found")

    if movie_id not in user_movie.movies:
        user_movie.movies.append(movie_id)

    session.add(user_movie)
    session.commit()
    session.refresh(user_movie)

    return user_movie


def remove_userMovie(*, session: SessionDep, current_user: CurrentUser, movie_id: int) -> UserMovie:
    """
    Remove a movie id to movies in usermovie table
    """
    user_movie = session.get(UserMovie, current_user.id)
    if not user_movie:
        raise ValueError(f"UserMovie with User ID {current_user.id} not found")
    
    if movie_id in user_movie.movies:
        user_movie.movies.remove(movie_id)
    
    session.add(user_movie)
    session.commit()
    session.refresh(user_movie)

    return user_movie

