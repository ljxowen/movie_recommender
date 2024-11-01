from sqlalchemy import create_engine
import os

#这个函数从环境变量中获取数据库连接信息，并构建一个数据库 URL。
def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "0427")
    #server = os.getenv("POSTGRES_SERVER", "db")
    server = "localhost"
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"

url = get_url()
print(f"Database URL: {url}")

engine = create_engine(url)
connection = engine.connect()
print("Successful connect to database")
connection.close()