
#这些导入语句引入了所需的模块和库，包括 SQLModel 的会话、创建引擎、选择语句，以及应用程序的配置、CRUD 操作和用户模型。
from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.crud import users
from app.models.user import User, UserCreate

#这行代码创建了一个数据库引擎。settings.SQLALCHEMY_DATABASE_URI 包含了数据库连接 URI，该 URI 是根据先前定义的配置生成的。
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


#在初始化数据库之前，确保所有 SQLModel 模型已经被导入。这是为了确保模型之间的关系能够正确初始化。
# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


#定义了一个 init_db 函数，用于初始化数据库。这个函数接受一个 SQLModel 的会话对象 session。
def init_db(session: Session) -> None:
    #这段注释建议使用 Alembic 进行数据库迁移，而不是直接创建表。如果不使用迁移，可以取消注释相应的代码来创建表。
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    #这行代码查询数据库，检查是否存在一个具有 FIRST_SUPERUSER 电子邮件的用户。
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    #如果没有找到超级用户，就创建一个新的 UserCreate 对象，并使用 users.create_user 函数将其添加到数据库中。
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = users.create_user(session=session, user_create=user_in)

"""
功能实例
假设 .env 文件中有以下配置：
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=supersecurepassword

在初始化数据库时，init_db 函数会执行以下步骤：
创建一个数据库会话：
session = Session(engine)

调用init_db函数：
init_db(session)

init_db 函数首先查询是否存在 admin@example.com 的用户，
如果没有找到这个用户，则创建一个新的超级用户：
"""