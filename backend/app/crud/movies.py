
from sqlmodel import create_engine, Session, select, func
from app.models.omdb_movie import Movie, MovieCreateIn, MoviesPublicOut
from app.models.user_movie import UserMovie
from app.api.deps import SessionDep, CurrentUser

#创建movie实例并添加到数据库中
def create_movie(*, session: Session, movie_in: MovieCreateIn, owner_id: int) -> Movie:
    # 创建 Movie 实例
    db_movie = Movie.model_validate(
        movie_in,
        update={"owner_id": owner_id}
    )
    # 添加到会话中
    session.add(db_movie)
    session.commit()
    # 刷新会话以获取最新的数据
    session.refresh(db_movie)
    
    return db_movie


def read_movies_by_ids(session: SessionDep, current_user: CurrentUser) -> MoviesPublicOut:
    """
    Get Movies by IDs
    """
    user_movie = session.get(UserMovie, current_user.id)
    if not user_movie:
        raise ValueError(f"UserMovie with User ID {current_user.id} not found")
    
    ids = user_movie.movies

    count_statement = (
        select(func.count())
        .select_from(Movie)
        .where(Movie.id.in_(ids))
    )
    count = session.exec(count_statement).one()

    statement = (
        select(Movie)
        .where(Movie.id.in_(ids))
    )
    movies = session.exec(statement).all()
    if not movies:
        raise ValueError(f"Movies Not found {ids}")

    return MoviesPublicOut(data=movies, count=count)