#这段代码涉及电子邮件发送和密码重置功能
"""
    logging：用于记录日志信息。
    dataclasses.dataclass：用于创建数据类 EmailData。
    datetime 和 timedelta：用于处理日期和时间。
    pathlib.Path：用于处理文件路径。
    typing.Any：用于类型注解。
    emails：用于发送电子邮件。
    jinja2.Template：用于渲染 HTML 模板。
    jose.JWTError 和 jose.jwt：用于生成和验证 JSON Web Token (JWT)。
    settings：包含应用程序的配置参数。
"""
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import emails  # type: ignore
from jinja2 import Template
from jose import JWTError, jwt

from app.core.config import settings


# EmailData：一个数据类，包含电子邮件的 HTML 内容和主题。
@dataclass
class EmailData:
    html_content: str
    subject: str


"""渲染电子邮件模板
    render_email_template：渲染电子邮件模板函数。
        template_name：模板文件名。
        context：上下文数据，用于渲染模板。
        返回值：渲染后的 HTML 内容。
"""
def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


"""发送电子邮件
    send_email：发送电子邮件函数。
        email_to：收件人电子邮件地址。
        subject：电子邮件主题。
        html_content：电子邮件内容。
        smtp_options：SMTP 配置参数。
        使用 emails 库发送电子邮件，并记录发送结果。
"""
def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logging.info(f"send email result: {response}")


"""生成测试电子邮件
    generate_test_email：生成测试电子邮件数据。
        email_to：收件人电子邮件地址。
        返回值：EmailData 包含渲染后的 HTML 内容和主题。
"""
def generate_test_email(email_to: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


"""生成密码重置电子邮件
    generate_reset_password_email：生成密码重置电子邮件数据。
        email_to：收件人电子邮件地址。
        email：用户名或电子邮件地址。
        token：密码重置令牌。
        返回值：EmailData 包含渲染后的 HTML 内容和主题。
"""
def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.server_host}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


"""生成新账户电子邮件
    generate_new_account_email：生成新账户电子邮件数据。
        email_to：收件人电子邮件地址。
        username：用户名。
        password：密码。
        返回值：EmailData 包含渲染后的 HTML 内容和主题。
"""
def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.server_host,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


"""生成密码重置令牌
    generate_password_reset_token：生成密码重置令牌。
        email：用户的电子邮件地址。
        返回值：JWT 编码的密码重置令牌。
"""
def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


"""验证密码重置令牌
    verify_password_reset_token：验证密码重置令牌。
        token：密码重置令牌。
        返回值：如果令牌有效，返回电子邮件地址；否则返回 None。
"""
def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return str(decoded_token["sub"])
    except JWTError:
        return None
    


"""
总结
    邮件模板渲染：使用 Jinja2 模板引擎渲染邮件内容。
    邮件发送：使用 emails 库发送邮件，通过 SMTP 配置发送参数。
    邮件生成：提供生成测试邮件、新账户邮件和密码重置邮件的功能。
    JWT 生成和验证：使用 jose 库生成和验证 JWT，用于密码重置令牌的处理。
"""