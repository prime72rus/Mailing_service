from django.urls import path

# from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (
    index_view,
    MailingListView,
    MailingDetailView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    RecipientListView,
    RecipientDetailView,
    RecipientCreateView,
    RecipientUpdateView,
    RecipientDeleteView,
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    LogListView,
    send_mailing_view,
    complete_mailing_view,
)

app_name = MailingConfig.name

urlpatterns = [
    path("mailing/", index_view, name="index"),
    path("mailing/list/", MailingListView.as_view(), name="mailing_list"),
    path(
        "mailing/<int:pk>/detail",
        MailingDetailView.as_view(),
        name="mailing_detail",
    ),
    path("mailing/create", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing/<int:pk>/update",
        MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailing/<int:pk>/delete",
        MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path(
        "recipient/list/", RecipientListView.as_view(), name="recipient_list"
    ),
    path(
        "recipient/<int:pk>/detail",
        RecipientDetailView.as_view(),
        name="recipient_detail",
    ),
    path(
        "recipient/create",
        RecipientCreateView.as_view(),
        name="recipient_create",
    ),
    path(
        "recipient/<int:pk>/update",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/<int:pk>/delete",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("message/list/", MessageListView.as_view(), name="message_list"),
    path(
        "message/<int:pk>/detail",
        MessageDetailView.as_view(),
        name="message_detail",
    ),
    path("message/create", MessageCreateView.as_view(), name="message_create"),
    path(
        "message/<int:pk>/update",
        MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "message/<int:pk>/delete",
        MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("log/list/", LogListView.as_view(), name="logs"),
    path("mailing/<int:pk>/send/", send_mailing_view, name="mailing_send"),
    path("mailing/<int:pk>/complete/", complete_mailing_view, name="mailing_complete"),
]
