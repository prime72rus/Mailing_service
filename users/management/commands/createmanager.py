import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from getpass import getpass
from users.models import User
from mailing.models import Mailing, Message, Recipient, Log
from itertools import chain


class Command(BaseCommand):
    help = "Создает пользователя с правами менеджера (email + пароль)"

    def handle(self, *args, **options):
        email = input("Введите email пользователя: ").strip()
        while not email:
            self.stdout.write(self.style.ERROR("Email не может быть пустым!"))
            email = input("Введите email пользователя: ").strip()

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR("Пользователь с "
                                               "таким email уже существует!"))
            return

        password = getpass("Введите пароль: ").strip()
        while not password:
            self.stdout.write(self.style.ERROR("Пароль не может быть пустым!"))
            password = getpass("Введите пароль: ").strip()

        user = User.objects.create(
            email=email,
            is_active=True,
            token=secrets.token_hex(16)
        )

        user.set_password(password)
        user.save()

        manager_group, created = Group.objects.get_or_create(name="Managers")

        if created:
            user_perms = Permission.objects.filter(
                content_type=ContentType.objects.get_for_model(User),
                codename__in=["view_user", "can_blocked_user"]
            )
            mailing_perms = Permission.objects.filter(
                content_type=ContentType.objects.get_for_model(Mailing),
                codename__in=["view_mailing", "can_disable_mailing"]
            )
            log_perms = Permission.objects.filter(
                content_type=ContentType.objects.get_for_model(Log),
                codename__in=['view_log']
            )
            recipient_perms = Permission.objects.filter(
                content_type=ContentType.objects.get_for_model(Recipient),
                codename__in=["view_recipient"]
            )
            message_perms = Permission.objects.filter(
                content_type=ContentType.objects.get_for_model(Message),
                codename__in=["view_message"]
            )

            all_permissions = list(chain(
                user_perms,
                mailing_perms,
                log_perms,
                recipient_perms,
                message_perms
            ))

            manager_group.permissions.add(*all_permissions)

            self.stdout.write(self.style.SUCCESS(
                'Создана группа "Managers"'))

        user.groups.add(manager_group)

        users_group = Group.objects.get(name="Users")
        user.groups.remove(users_group)

        self.stdout.write(
            self.style.SUCCESS(
                f"Пользователь {email} создан как менеджер."
            )
        )
