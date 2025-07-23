# -*- coding=utf-8 -*-
r"""

"""
from email.message import EmailMessage
from pathlib import Path
import aiosmtplib
import jinja2
from app.config import SETTINGS
from .lib import TO, normalize_to


__all__ = ['SUPPORTED', 'render_template', 'send_email']


SUPPORTED: bool = SETTINGS.MAIL is not None


TEMPLATE_DIR = Path(__file__).parent / "templates"

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [SETTINGS.MAIL.TEMPLATES_DIR, TEMPLATE_DIR]
        if SETTINGS.MAIL and SETTINGS.MAIL.TEMPLATES_DIR
        else TEMPLATE_DIR,
    ),
    autoescape=jinja2.select_autoescape([".html.j2"]),
    enable_async=True,
)


async def render_template(name: str, context: dict) -> str:
    template = jinja_env.get_template(name)
    return await template.render_async(context)


async def send_email(to: TO, subject: str, html_body: str):
    if not SUPPORTED:
        raise RuntimeError("No MAIL configured")

    message = EmailMessage()
    message['From'] = str(SETTINGS.MAIL.FROM)
    message['To'] = normalize_to(to)
    message['Subject'] = subject
    message.set_content("This is an HTML email. Please view it in an HTML-compatible client.")  # todo: automatic fallback conversion from html->text
    message.add_alternative(html_body, subtype="html")

    async with aiosmtplib.SMTP(
            hostname=SETTINGS.MAIL.SERVER,
            port=SETTINGS.MAIL.PORT,
            use_tls=SETTINGS.MAIL.USE_TLS,
            start_tls=SETTINGS.MAIL.START_TLS,
            validate_certs=SETTINGS.MAIL.VALIDATE_CERTS,
    ) as smtp:
        if SETTINGS.MAIL.USE_CREDENTIALS:
            await smtp.login(SETTINGS.MAIL.USERNAME, SETTINGS.MAIL.PASSWORD.get_secret_value())
        await smtp.send_message(message)
