from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from mailing.models import Recipient, Mailing, Message, Log
from users.models import User
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.core.mail import send_mail
from mailing.forms import MailingForm, RecipientForm, MessageForm
from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
def index_view(request):
    user = request.user

    all_mailings = Mailing.objects.all()
    active_mailings = all_mailings.filter(status="launched")
    unique_recipients = Recipient.objects.values("email").distinct()

    all_logs = Log.objects.all()
    saccess_logs = all_logs.filter(status="successfully")
    failure_logs = all_logs.filter(status="failure")

    if user.is_authenticated:
        user_mailings = all_mailings.filter(owner=user).count()
        user_active_mailings = active_mailings.filter(owner=user).count()
        user_recipients = Recipient.objects.filter(owner=user).count()

        user_logs = all_logs.filter(owner=user).count
        user_saccess_logs = saccess_logs.filter(owner=user).count()
        user_failure_logs = failure_logs.filter(owner=user).count()

    else:
        user_mailings = user_active_mailings = user_recipients = user_logs = user_saccess_logs = user_failure_logs = 0

    context = {
        "all_mailings": all_mailings.count(),
        "active_mailings": active_mailings.count(),
        "unique_recipients": unique_recipients.count(),
        "user_mailings": user_mailings,
        "user_active_mailings": user_active_mailings,
        "user_recipients": user_recipients,

        "all_logs": all_logs.count(),
        "saccess_logs": saccess_logs.count(),
        "failure_logs": failure_logs.count(),
        "user_logs": user_logs,
        "user_saccess_logs": user_saccess_logs,
        "user_failure_logs": user_failure_logs,
    }

    return render(request, "mailing/index.html", context)


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    permission_required = "mailing.view_mailing"
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.groups.filter(
                name='Managers').exists() or self.request.user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                        DetailView):
    model = Mailing
    permission_required = "mailing.view_mailing"
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.object

        logs = mailing.logs.all()
        context["success_count"] = logs.filter(status="successfully").count()
        context["not_success_count"] = logs.filter(status="failure").count()
        if self.request.user.groups.filter(
                name='Managers').exists() or self.request.user.is_superuser:
            context["logs_count"] = logs.count()
        else:
            context["logs_count"] = logs.filter(owner=self.request.user).count()

        return context


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                        CreateView):
    model = Mailing
    permission_required = "mailing.add_mailing"
    form_class = MailingForm
    template_name = "mailing/mailing_create.html"

    def get_success_url(self):
        return reverse(
            "mailing:mailing_detail",
            kwargs={'pk': self.object.pk}
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                        UpdateView):
    model = Mailing
    permission_required = "mailing.change_mailing"
    form_class = MailingForm
    template_name = "mailing/mailing_update.html"

    def get_success_url(self):
        return reverse(
            "mailing:mailing_detail",
            kwargs={'pk': self.object.pk}
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.status = "created"
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                        DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    permission_required = "mailing.delete_mailing"
    success_url = reverse_lazy("mailing:mailing_list")


@login_required
def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if not request.user.is_superuser and mailing.owner != request.user:
        return HttpResponseForbidden("У вас нет доступа к этой рассылке")

    recipients = mailing.recipients.all()
    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            status = "successfully"
            server_response = "Ок"
        except Exception as e:
            status = "failure"
            server_response = str(e)

        Log.objects.create(
            status=status,
            server_response=server_response,
            mailing=mailing,
            owner=request.user
        )

        mailing.status = "launched"
        mailing.save()

    return redirect('mailing:mailing_detail', pk=mailing.pk)


@login_required
def complete_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if not request.user.is_superuser and mailing.owner != request.user and not request.user.groups.filter(
                name='Managers').exists():
        return HttpResponseForbidden("У вас нет доступа для отключения рассылки")

    mailing.status = "completed"
    mailing.save()

    return redirect('mailing:mailing_detail', pk=mailing.pk)


class RecipientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Recipient
    permission_required = "mailing.view_recipient"
    template_name = "mailing/recipient_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        if self.request.user.groups.filter(
                name='Managers').exists() or self.request.user.is_superuser:
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                          DetailView):
    model = Recipient
    permission_required = "mailing.view_recipient"
    template_name = "mailing/recipient_detail.html"
    context_object_name = "recipient"


class RecipientCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                          CreateView):
    model = Recipient
    permission_required = "mailing.add_recipient"
    form_class = RecipientForm
    template_name = "mailing/recipient_create.html"

    def get_success_url(self):
        return reverse("mailing:recipient_detail",
                       kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                          UpdateView):
    model = Recipient
    permission_required = "mailing.change_recipient"
    form_class = RecipientForm
    template_name = "mailing/recipient_update.html"

    def get_success_url(self):
        return reverse("mailing:recipient_detail",
                       kwargs={'pk': self.object.pk})


class RecipientDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                          DeleteView):
    model = Recipient
    template_name = "mailing/recipient_delete.html"
    permission_required = "mailing.delete_recipient"
    success_url = reverse_lazy("mailing:recipient_list")


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    permission_required = "mailing.view_message"
    template_name = "mailing/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.groups.filter(
                name='Managers').exists() or self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                        DetailView):
    model = Message
    permission_required = "mailing.view_message"
    template_name = "mailing/message_detail.html"
    context_object_name = "message"


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                        CreateView):
    model = Message
    permission_required = "mailing.add_message"
    form_class = MessageForm
    template_name = "mailing/message_create.html"

    def get_success_url(self):
        return reverse("mailing:message_detail", kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                        UpdateView):
    model = Message
    permission_required = "mailing.change_message"
    form_class = MessageForm
    template_name = "mailing/message_update.html"

    def get_success_url(self):
        return reverse("mailing:message_detail", kwargs={'pk': self.object.pk})


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                        DeleteView):
    model = Message
    permission_required = "mailing.delete_message"
    template_name = "mailing/message_delete.html"
    success_url = reverse_lazy("mailing:message_list")


class LogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Log
    permission_required = "mailing.view_log"
    template_name = "mailing/log_list.html"
    context_object_name = "logs"

    def get_queryset(self):
        if self.request.user.groups.filter(
                name='Managers').exists() or self.request.user.is_superuser:
            return Log.objects.all()
        return Log.objects.filter(owner=self.request.user)
