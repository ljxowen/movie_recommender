
#这些导入语句引入了所需的模块和库，包括日期时间操作、类型注解、JWT 编码/解码、密码哈希以及应用程序的配置。
from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

#创建一个密码加密上下文，使用 bcrypt 算法对密码进行加密和验证。
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#定义了用于 JWT 编码的算法，这里使用的是 HS256 算法（HMAC-SHA256）。
ALGORITHM = "HS256"

#这个函数用于创建 JWT 访问令牌。具体步骤如下：
"""
计算过期时间：使用当前时间加上传入的 expires_delta 生成令牌的过期时间。
生成编码数据：创建一个包含过期时间 (exp) 和主题 (sub) 的字典。
编码 JWT：使用 jose 库将字典编码成 JWT，使用 settings.SECRET_KEY 作为密钥，并指定 HS256 算法。
返回令牌：返回生成的 JWT。
"""
def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#这个函数用于验证用户输入的密码是否与存储的哈希密码匹配。
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#这个函数用于生成密码的哈希值。
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


"""
实例解释
假设有一个用户注册过程，用户输入了他们的电子邮件和密码。一下是如何使用这些功能

用户注册：

email = "user@example.com"
password = "userpassword"

# 获取密码哈希
hashed_password = get_password_hash(password)

# 创建用户并保存到数据库（假设有一个 save_user 函数）
save_user(email=email, hashed_password=hashed_password)

用户登录：
# 假设从数据库获取用户的哈希密码
stored_hashed_password = get_user_hashed_password(email)

# 验证输入的密码是否匹配
if verify_password("userpassword", stored_hashed_password):
    # 创建访问令牌
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(subject=email, expires_delta=access_token_expires)
    print(f"Access Token: {access_token}")
else:
    print("Invalid credentials")
"""