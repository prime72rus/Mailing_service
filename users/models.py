from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    token = models.CharField(
        max_length=100, verbose_name="Токен", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_blocked_user", "Can blocked user"),
        ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        if created:
            group = Group.objects.get(name="Users")
            self.groups.add(group)
