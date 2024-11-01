from sqlmodel import create_engine, Session
from app.models.omdb_movie import MovieCreateIn
from app.crud.movies import create_movie  # 导入你定义的 create_movie 方法
from typing import Dict, Any

from app.core.config import settings

# 创建数据库引擎
#这行代码创建了一个数据库引擎。settings.SQLALCHEMY_DATABASE_URI 包含了数据库连接 URI，该 URI 是根据先前定义的配置生成的。
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

#创建数据库model格式的电影对象
def init_movie(session: Session, movie_data: Dict[str, Any], owner_id) -> None:
    movie_in = MovieCreateIn(
        title=movie_data['Title'],
        year=movie_data['Year'],
        rated=movie_data['Rated'],
        released=movie_data['Released'],
        runtime=movie_data['Runtime'],
        genre=movie_data['Genre'],
        director=movie_data['Director'],
        writer=movie_data['Writer'],
        actors=movie_data['Actors'],
        plot=movie_data['Plot'],
        language=movie_data['Language'],
        country=movie_data['Country'],
        awards=movie_data['Awards'],
        poster=movie_data['Poster'],
        imdb_rating=movie_data.get('imdbRating'),
        imdb_votes=movie_data.get('imdbVotes'),
        imdb_id=movie_data['imdbID'],
        metascore=movie_data.get('Metascore'),
        box_office=movie_data.get('BoxOffice'),
        production=movie_data.get('Production'),
        website=movie_data.get('Website')
    )
    
    movie = create_movie(session=session, movie_in=movie_in, owner_id=owner_id)
    print(f"Inserted movie: {movie.title}")

