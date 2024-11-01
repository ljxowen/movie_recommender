"""
这个 deps.py 文件定义了一些依赖项和辅助函数，用于在 FastAPI 应用中处理数据库会话和用户认证。
这些依赖项和辅助函数主要用于确保 API 请求的用户已认证，并具备适当的权限。以下是对每个部分的详细解释：
"""

#导入各种库和模块，用于依赖注入、异常处理、JWT 解码和数据库会话管理。
#OAuth2PasswordBearer 用于处理 OAuth2 认证。
#jwt 和 JWTError 用于处理 JWT 令牌的解码和错误。
#Session 用于与数据库交互。
#导入应用程序的配置和模型。
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models.user import TokenPayload, User

#创建一个 OAuth2PasswordBearer 实例，用于处理认证令牌。tokenUrl 是获取令牌的端点。
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


#创建一个生成器函数 get_db，用于管理数据库会话的生命周期。
#使用 Session(engine) 创建一个新的数据库会话，并在请求结束后自动关闭。
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


#SessionDep：使用 Annotated 结合 Depends(get_db)，定义数据库会话依赖项。
#TokenDep：使用 Annotated 结合 Depends(reusable_oauth2)，定义 OAuth2 令牌依赖项。
SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


#解码并验证 JWT 令牌。
#提取用户 ID（sub）并从数据库中获取用户。
#检查用户是否存在且活跃。
#返回用户对象，如果验证失败或用户无效则抛出 HTTP 异常。
def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


#使用 Annotated 结合 Depends(get_current_user)，定义当前用户依赖项。
CurrentUser = Annotated[User, Depends(get_current_user)]

#检查当前用户是否为超级用户。
#如果不是超级用户，抛出 HTTP 异常。
#如果是超级用户，返回当前用户对象。
def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user










