from django.core.mail import EmailMessage
from django.conf import settings


class SendNotificationEmail:
    def __init__(self, subject, email, message):
        self.subject = subject
        self.email   = email
        self.message = message

    def send_notification_email(self) -> bool:
        try:
            sent_mail = EmailMessage(
                subject=self.subject,
                body=self.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[self.email]
            )
            sent_mail.send()
            return True
        except Exception as e:
            return str(f'Error -> {e}')