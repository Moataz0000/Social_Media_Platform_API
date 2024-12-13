from celery import  shared_task
from django.core.management.sql import emit_post_migrate_signal

from .utils import SendNotificationEmail


@shared_task()
def send_verification_email_task(email, activation_link) -> bool:
    subject = 'Verify Your Email'
    message = f'Please, verify your email by clicking the link below:\n{activation_link}'
    try:
        email_sender = SendNotificationEmail(subject, email, message)
        email_sender.send_notification_email()
        return 'Task executed successfully.'
    except Exception as e:
        return str(f'Error -> {e}')



@shared_task()
def send_congratulations_email(email):
    subject = f'Congratulations, {email}'
    message = 'Your account has been successfully activated! Welcome to our platform.'
    try:
        email_sender = SendNotificationEmail(subject, email, message)
        email_sender.send_notification_email()
        return 'Task Executed Successfully.'
    except Exception as e:
        return str(e)


@shared_task()
def send_reset_password_email(email, reset_password_link):
    subject = 'Reset your password'
    message = f'Click this link to reset your password: {reset_password_link}'
    try:
        email_sender = SendNotificationEmail(subject, email, message)
        email_sender.send_notification_email()
        return 'Task Execute Successfully.'
    except Exception as e:
        return str(e)


@shared_task()
def send_email_after_reset(email):
    subject = 'Password Reset Successfully.'
    message = 'We could tell you your password changed successfully.'
    try:
        email_sender = SendNotificationEmail(subject, email, message)
        email_sender.send_notification_email()
        return 'Task Execute Successfully.'
    except Exception as e:
        return str(e)
