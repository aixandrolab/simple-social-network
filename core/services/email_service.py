import logging

from typing import List, Optional, Dict, Any, Union

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)


class EmailService:

    def __init__(self):
        pass

    @staticmethod
    def send_simple(
            subject: str,
            message: str,
            to: list[str],
            from_email: Optional[str],
            is_html: bool = False
    ) -> bool:
        try:
            send_mail(
                subject=subject,
                message=strip_tags(message) if is_html else message,
                from_email=from_email or settings.DEFAULT_FROM_EMAIL,
                recipient_list=to,
                fail_silently=False,
                html_message=message if is_html else None,
            )
            logger.info(f"Email sent to: {to}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    @staticmethod
    def send_template(
            subject: str,
            template: str,
            context: Dict[str, Any],
            to: List[str],
            from_email: Optional[str] = None
    ) -> bool:
        try:
            html_body = render_to_string(template, context)

            text_body = strip_tags(html_body)

            send_mail(
                subject=subject,
                message=text_body,
                from_email=from_email or settings.DEFAULT_FROM_EMAIL,
                recipient_list=to,
                fail_silently=False,
                html_message=html_body,
            )
            logger.info(f"Template email sent to: {to}")
            return True
        except Exception as e:
            logger.error(f"Failed to sent template email: {e}")
            return False

class VerificationEmail:

    @staticmethod
    def send(user_email: str, verification_url: str, username: str) -> bool:
        return EmailService.send_template(
            subject='Email Verification',
            template='emails/verification_template.html',
            context={
                'username': username,
                'verification_url': verification_url,
                'site_name': getattr(settings, 'SITE_NAME', 'Simple Social Network')
            },
            to=[user_email],
        )

class PasswordResetEmail:

    @staticmethod
    def send(user_email: str, reset_url: str, username: str) -> bool:
        return EmailService.send_template(
            subject="Password Reset",
            template="emails/password_reset_template.html",
            context={
                'username': username,
                'reset_url': reset_url,
                'site_name': getattr(settings, 'SITE_NAME', 'Simple Social Network')
            },
            to=[user_email]
        )

class NotificationEmail:

    @staticmethod
    def send(user_email: str, title: str, message: str, action_url: Optional[str]=None) -> bool:
        return EmailService.send_template(
            subject=title,
            template='emails/notification_template.html',
            context={
                'title': title,
                'message': message,
                'action_url': action_url,
                'action_desc': "Go to" if action_url else None,
            },
            to=[user_email]
        )

class WelcomeEmail:

    @staticmethod
    def send(user_email: str, username: str) -> bool:
        return EmailService.send_template(
            subject="Welcome!!!",
            template="emails/welcome_template.html",
            context={
                'username': username,
                'site_name': getattr(settings, 'SITE_NAME', 'Simple Social Network')
            },
            to=[user_email]
        )

class Email:

    @staticmethod
    def send(subject: str, message: str, to: Union[str, List[str]], from_email: str, is_html: bool = False) -> bool:
        to_list = [to] if isinstance(to, str) else to
        return EmailService().send_simple(subject, message, to_list, from_email, is_html)

    @staticmethod
    def template(template_path: str, context: Dict, to: Union[str, List[str]], subject: str = '') -> bool:
        to_list = [to] if isinstance(to, str) else to
        if not subject:
            subject = context.get('subject', 'Notification')
        return EmailService().send_template(subject, template_path, context, to_list)

    @staticmethod
    def verification(to: str, url: str, username: str) -> bool:
        return VerificationEmail.send(to, url, username)

    @staticmethod
    def reset_password(to: str, url: str, username: str) -> bool:
        return PasswordResetEmail.send(to, url, username)

    @staticmethod
    def notification(to: str, title: str, message: str, action_url: str = '') -> bool:
        return NotificationEmail.send(to, title, message, action_url)

    @staticmethod
    def welcome(to: str, username: str) -> bool:
        return WelcomeEmail.send(to, username)
