from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from mailing.models import Recipient, Mailing, Message, Log
from users.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from mailing.forms import MailingForm, RecipientForm


def index_view(request):
    user = request.user

    all_mailings = Mailing.objects.all()
    active_mailings = all_mailings.filter(status="launched")
    unique_recipients = Recipient.objects.values("email").distinct()

    if user.is_authenticated:
        user_mailings = all_mailings.filter(owner=user).count()
        user_active_mailings = active_mailings.filter(owner=user).count()
        user_recipients = Recipient.objects.filter(owner=user).count()
    else:
        user_mailings = user_active_mailings = user_recipients = 0

    context = {
        "all_mailings": all_mailings.count(),
        "active_mailings": active_mailings.count(),
        "unique_recipients": unique_recipients.count(),
        "user_mailings": user_mailings,
        "user_active_mailings": user_active_mailings,
        "user_recipients": user_recipients,
    }

    return render(request, "mailing/index.html", context)


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    permission_required = "mailing.view_mailing"
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists() or self.request.user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    permission_required = "mailing.view_mailing"
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Mailing
    permission_required = "mailing.add_mailing"
    form_class = MailingForm
    template_name = "mailing/mailing_create.html"

    def get_success_url(self):
        return reverse("mailing:mailing_detail", kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = "Создана"
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    permission_required = "mailing.change_mailing"
    form_class = MailingForm
    template_name = "mailing/mailing_update.html"

    def get_success_url(self):
        return reverse("mailing:mailing_detail", kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.status = "created"
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    permission_required = "mailing.delete_mailing"
    success_url = reverse_lazy("mailing:mailing_list")


class RecipientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Recipient
    permission_required = "mailing.view_recipient"
    template_name = "mailing/recipient_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists() or self.request.user.is_superuser:
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Recipient
    permission_required = "mailing.view_recipient"
    template_name = "mailing/recipient_detail.html"
    context_object_name = "recipient"


class RecipientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Recipient
    permission_required = "mailing.add_recipient"
    form_class = RecipientForm
    template_name = "mailing/recipient_create.html"

    def get_success_url(self):
        return reverse("mailing:recipient_detail", kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    permission_required = "mailing.change_recipient"
    form_class = RecipientForm
    template_name = "mailing/recipient_update.html"

    def get_success_url(self):
        return reverse("mailing:recipient_detail", kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailing/recipient_delete.html"
    permission_required = "mailing.delete_recipient"
    success_url = reverse_lazy("mailing:recipient_list")


class MessageListView(LoginRequiredMixin, ListView):
    pass


class MessageDetailView(LoginRequiredMixin, DetailView):
    pass


class MessageCreateView(LoginRequiredMixin, CreateView):
    pass


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    pass


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    pass


class LogListView(LoginRequiredMixin, ListView):
    pass
