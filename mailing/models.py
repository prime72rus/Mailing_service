from django.db import models
from users.models import User


class Recipient(models.Model):

    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=100, verbose_name="ФИО клиента")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="recipients",
        verbose_name="Владелец записи получатель",
    )

    def __str__(self):
        return self.full_name

    class Meta:

        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"


class Mailing(models.Model):

    PERIOD_CHOICES = [
        ("daily", "Ежедневно"),
        ("once_week", "Раз в неделю"),
        ("once_month", "Раз в месяц"),
    ]

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("launched", "Запущена"),
        ("completed", "Завершена"),
    ]

    datetime_start = models.DateTimeField(verbose_name="Начало")
    datetime_end = models.DateTimeField(verbose_name="Окончание")
    period = models.CharField(
        max_length=15,
        choices=PERIOD_CHOICES,
        default="daily",
        verbose_name="Периодичность",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="created",
        verbose_name="Статус",
    )
    message = models.ForeignKey(
        "Message",
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение",
    )
    recipients = models.ManyToManyField(
        "Recipient", related_name="mailings", verbose_name="Получатели"
    )
    owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Владелец рассылки",
    )

    def __str__(self):
        return f"{self.id} {self.status}"

    class Meta:

        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_disable_mailing", "Can disable mailing"),
        ]


class Message(models.Model):

    subject = models.CharField(max_length=200, verbose_name="Тема")
    content = models.TextField(verbose_name="Сообщение")
    owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Владелец сообщения",
    )

    def __str__(self):
        return self.subject

    class Meta:

        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Log(models.Model):

    STATUS_CHOICES = [
        ("successfully", "Успешно"),
        ("failure", "Неудачно"),
    ]

    datetime_log = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    server_response = models.TextField(verbose_name="Ответ сервера")
    mailing = models.ForeignKey(
        "Mailing",
        on_delete=models.CASCADE,
        related_name="logs",
        verbose_name="Рассылка",
    )
    owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="logs",
        verbose_name="Владелец записи лога попытки",
    )

    def __str__(self):
        return f"{self.id} - {self.status}"

    class Meta:

        verbose_name = "Лог"
        verbose_name_plural = "Логи"
