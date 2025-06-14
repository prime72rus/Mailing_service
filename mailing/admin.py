from django.contrib import admin

from mailing.models import Log, Mailing, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "owner")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "owner")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "owner")


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "mailing", "owner")
