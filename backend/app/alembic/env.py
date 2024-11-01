#这些导入语句引入了所需的模块和库，包括操作系统环境变量、日志配置、Alembic 的上下文和 SQLAlchemy 的引擎和连接池。
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

#context.config 是 Alembic 的配置对象，用于访问配置文件中的值。
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

#这行代码设置了日志配置，使用 Alembic 配置文件中指定的日志配置文件。
# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name) # type: ignore


#这部分代码导入了应用程序中的模型，并设置了 target_metadata 为这些模型的元数据。target_metadata 用于支持自动生成迁移脚本。
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
#在 alembic/env.py 文件中导入这些模型类的原因是确保它们的元数据对象被 Alembic 识别。
from app.models.user import SQLModel  # noqa
from app.models.omdb_movie import SQLModel # noqa
from app.models.user_movie import SQLModel # noqa

target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

#这个函数从环境变量中获取数据库连接信息，并构建一个数据库 URL。
def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "0427")
    server = os.getenv("POSTGRES_SERVER", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"


#这个函数用于在离线模式下运行迁移。在这种模式下，配置上下文仅使用数据库 URL，而不需要创建引擎。
#配置上下文后，开始一个事务并运行迁移。
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    #url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

#这个函数用于在在线模式下运行迁移。在这种模式下，需要创建一个引擎并与上下文关联。
#首先从配置中获取设置，然后创建引擎并连接到数据库。配置上下文后，开始一个事务并运行迁移。
def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()











