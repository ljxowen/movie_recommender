import requests
import logging

from sqlmodel import Session

from app.core.movie_db import engine, init_movie

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_movie_data(title):
    omdb_url = 'http://www.omdbapi.com/?'
    api_key = 'd3f0c7c3'
    params = {
        'apikey': api_key,
        't': title
    }
    response = requests.get(omdb_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return -1
    

def add_movies(movie_titles) -> None:
    logger.info("Adding movies data")
    owner_id = 1 # set superuser as default owner
    for title in movie_titles:
        movie_data = fetch_movie_data(title)
        if movie_data == -1:
            continue
        with Session(engine) as session:
            init_movie(session, movie_data, owner_id)
    logger.info("Movies data added")


def main() -> None:
    movie_titles = ["Inception", "The Matrix", "Interstellar", "The Shawshank Redemption", "The Godfather", "Forrest Gump",
                    "The Dark Knight", "Pulp Fiction", "Fight Club", "The Lord of the Rings: The Fellowship of the Ring"]
    add_movies(movie_titles)

if __name__ == "__main__":
    main()