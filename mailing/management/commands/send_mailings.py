from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from mailing.models import Mailing, Log


class Command(BaseCommand):
    help = 'Отправляет все рассылки со статусом "created" или "launched"'

    def handle(self, *args, **options):

        mailings = Mailing.objects.filter(status__in=["created", "launched"])

        if not mailings.exists():
            self.stdout.write(self.style.WARNING("Нет рассылок для отправки."))
            return

        self.stdout.write(f"Найдено рассылок: {mailings.count()}")

        for mailing in mailings:
            recipients = mailing.recipients.all()
            self.stdout.write(f"Обработка рассылки ID={mailing.id}...")
            for recipient in recipients:
                try:
                    self.stdout.write(f"Отправка получателю {recipient.email}")
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    status = "successfully"
                    server_response = "Ок"
                    self.stdout.write(self.style.SUCCESS("Успешно!"))
                except Exception as e:
                    status = "failure"
                    server_response = str(e)
                    self.stdout.write(self.style.ERROR(f"{e}"))

                Log.objects.create(
                    status=status,
                    server_response=server_response,
                    mailing=mailing,
                    owner=mailing.owner,
                )

            mailing.status = "launched"
            mailing.save()

        self.stdout.write(self.style.SUCCESS("Отправка сообщений завершена!"))
