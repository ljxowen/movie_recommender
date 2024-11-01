"""
这段代码定义了 FastAPI 应用中的路由，通过将不同的路由模块引入到主路由中，从而管理不同类别的 API 路由。
"""

#导入 FastAPI 的 APIRouter 类，用于创建 API 路由。
#导入应用程序中不同功能模块的路由。这些模块分别负责处理特定的业务逻辑，如用户管理、项目管理、员工管理等。
from fastapi import APIRouter

from app.api.routes import (
    movies,
    login,
    users,
    user_movie,
    utils,
)

#创建一个 APIRouter 实例，作为主路由，用于包含所有子路由。
api_router = APIRouter()

# 用户相关
#login.router：处理用户登录相关的路由。
#users.router：处理用户管理相关的路由，路由前缀为 /users，标签为 "用户 - users"。
api_router.include_router(login.router, tags=["登录 - /login"])
api_router.include_router(users.router, prefix="/users", tags=["用户 - users"])

# Movie 
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(user_movie.router, prefix="/user_movie", tags=["user_movie"])

# Other 
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])