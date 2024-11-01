#这些导入语句引入了所需的模块和库，包括生成随机密钥、发出警告、类型注解以及 Pydantic 用于数据验证和解析的功能
import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

#这是一个辅助函数，用于解析 CORS（跨源资源共享）设置。
#如果输入是一个逗号分隔的字符串，它将其转换为一个字符串列表。如果输入已经是列表或字符串，则返回该输入。否则，引发一个 ValueError。
def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

#定义了一个 Settings 类，继承自 BaseSettings，用于加载和管理配置。
#model_config 用于指定加载环境变量的文件（.env）以及其他配置选项。
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    #这些是一些基础配置项，包括 API 路径、生成的随机密钥、访问令牌过期时间、域名和环境（本地、预发布、生产）。
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    #这是一个计算属性，根据环境设置返回适当的服务器主机名。
    #例如，如果 ENVIRONMENT 是 local，那么 server_host 返回 http://localhost。
    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    #这个字段定义了后端 CORS 起源，使用了自定义的验证器 parse_cors 来处理输入。
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    #这些字段定义了项目名称、Sentry 数据源名称以及 PostgreSQL 数据库的相关配置。
    #例如，如果 .env 文件中有 BACKEND_CORS_ORIGINS=https://example.com, https://another.com，
    #那么解析后会成为一个列表：["https://example.com", "https://another.com"]。
    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""

    #这是另一个计算属性，用于构建 SQLAlchemy 数据库 URI。
    #例如，根据 .env 文件中的配置，生成的 URI 可能是 postgresql+psycopg://postgres_user:postgres_password@127.0.0.1:5432/。
    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    #这些字段定义了 SMTP 邮件服务器的相关配置。
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    #这是一个模型验证器，用于在实例化对象后设置默认的发件人名称。
    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    #这些字段和属性用于邮件重置令牌的过期时间以及检查邮件是否启用。
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    #这些字段定义了测试用户、超级用户以及是否开放用户注册。
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAIL_TEST_USER: str = "test@example.com"
    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    #这个方法用于检查某些敏感字段是否使用了默认值 changethis，并在生产环境中强制更改它们。
    #例如，如果 POSTGRES_PASSWORD 是 changethis，在非本地环境下会引发 ValueError，在本地环境下会发出警告。
    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    #这个模型验证器调用了 _check_default_secret 方法来确保敏感字段没有使用默认值。
    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self

#例化了 Settings 类，用于加载配置。
settings = Settings()  # type: ignore