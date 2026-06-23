import os

from configs.celery import app
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

UserModel = get_user_model()


@app.task
def send_email_task(to: str, template_name: str, context: dict, subject: str) -> None:
    template = get_template(template_name)
    html_content = template.render(context)

    msg = EmailMultiAlternatives(
        to=[to],
        from_email=os.environ.get('EMAIL_HOST_USER'),
        subject=subject,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


class EmailService:
    @classmethod
    def register(cls, user):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost/activate/{token}'

        send_email_task.delay(
            to=user.email,
            template_name="register.html",
            context={'name': user.profile.name, 'url': url},
            subject="Успішна реєстрація"
        )

    @classmethod
    def recovery(cls, user):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost/recovery/{token}'

        send_email_task.delay(
            to=user.email,
            template_name='recovery.html',
            context={'url': url},
            subject="Відновлення доступу"
        )

    @classmethod
    def manager_alert(cls, email: str, ad_id: int):
        url = f'http://localhost/moderation/ads/{ad_id}/'
        send_email_task.delay(
            to=email,
            template_name='manager_alert.html',
            context={'url': url, 'ad_id': ad_id},
            subject="Оголошення потребує перевірки менеджера"
        )