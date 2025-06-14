import secrets

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from users.models import User


def send_verification_email(user, request):
    """
    Функция генерирует токен и отправляет письмо для подтверждения почты
    """
    token = secrets.token_hex(16)
    user.token = token
    user.save()

    host = request.get_host()
    verification_url = f"http://{host}/email-confirm/{token}/"

    subject = "Добро пожаловать в наш сервис"
    message = (
        f"Спасибо, что зарегистрировались! Для подтверждения почты "
        f"перейдите по ссылке: {verification_url}"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def verify_user_email(token):
    """
    Функция активирует пользователя по токену и
    перенаправляет на страницу входа
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse("users:login"))
