# sentry_sdk：用于错误监控和报告工具 Sentry 的 SDK。
# FastAPI：FastAPI 框架的主要类，用于创建应用实例。
# APIRoute：FastAPI 中的路由类，用于定义和管理 API 路由。
# CORSMiddleware：Starlette 的中间件，用于处理跨源资源共享 (CORS)。
# api_router：自定义的路由器实例，包含应用程序的所有 API 路由。
# settings：应用程序的配置设置，包含各种配置参数。
import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

""" 自定义生成唯一ID的函数
这个函数用于生成路由的唯一 ID。
route：一个 APIRoute 实例。
返回值：一个字符串，由路由的第一个标签和路由的名称组成。这个函数主要用于 OpenAPI 文档生成时为每个路由生成唯一的 ID。
"""
def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

"""初始化Sentry
检查配置中是否提供了 Sentry 的 DSN（Data Source Name）并且当前环境不是本地开发环境。
如果条件满足，初始化 Sentry SDK，用于捕获和报告应用程序中的错误和异常。
"""
if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

"""创建FastAPI应用实例
title：设置 API 文档的标题，使用项目名称。
openapi_url：设置 OpenAPI 文档的 URL。
generate_unique_id_function：设置用于生成唯一 ID 的自定义函数。
"""
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

"""设置CORS中间件
检查配置中是否定义了 BACKEND_CORS_ORIGINS。
如果定义了，添加 CORS 中间件，允许跨源请求。
allow_origins：允许的源列表。
allow_credentials：是否允许发送凭据（如 Cookies）。
allow_methods：允许的 HTTP 方法。
allow_headers：允许的 HTTP 头。
"""
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

#包含 API 路由
#使用 include_router 方法将 api_router 包含到应用实例中。
#prefix：所有路由的前缀，即 API 的版本字符串。
app.include_router(api_router, prefix=settings.API_V1_STR)



"""
详细解释每个部分的目的和功能：
custom_generate_unique_id 函数
这个函数通过路由的第一个标签和路由的名称来生成唯一的 ID。
这在 OpenAPI 文档生成时很有用，因为它可以确保每个路由都有一个独特的标识符。

Sentry 初始化
这一部分代码检查是否提供了 Sentry 的 DSN 以及当前环境是否不是本地开发环境。
如果条件满足，则初始化 Sentry SDK。这意味着如果应用程序在生产或其他环境中运行并且配置了 Sentry，
任何未捕获的异常将被自动发送到 Sentry，以便开发者可以监控和修复这些问题。

创建 FastAPI 应用实例
使用 FastAPI 类创建应用实例，并设置 API 文档的标题和 URL，还指定了自定义的唯一 ID 生成函数。

CORS 中间件
CORS（跨源资源共享）中间件允许你的 API 能够处理来自不同源的请求。
这里的代码从配置中读取允许的源，并相应地设置 CORS 规则。
这样，可以确保你的 API 能够被前端应用程序或其他服务访问。

包含 API 路由
最后，代码包含了自定义的 API 路由器（api_router），并为所有路由添加了一个前缀（即 API 版本字符串）。
这使得 API 的路由结构更加清晰和组织化。
"""