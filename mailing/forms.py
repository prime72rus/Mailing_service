import os
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from mailing.models import Mailing, Recipient, Message


class MailingForm(forms.ModelForm):

    class Meta:

        model = Mailing
        exclude = ["owner", "status"]
        widgets = {
            "datetime_start": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "datetime_end": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["period"].widget.attrs.update({
            "class": "form-control",
        })
        self.fields["message"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["recipients"].widget.attrs.update({
            "class": "form-control",
        })

        if self.user:
            if self.user.is_superuser:
                self.fields["recipients"].queryset = Recipient.objects.all()
                self.fields['message'].queryset = Message.objects.all()
            else:
                self.fields["recipients"].queryset = Recipient.objects.filter(owner=self.user)
                self.fields["message"].queryset = Message.objects.filter(owner=self.user)


class RecipientForm(forms.ModelForm):

    class Meta:

        model = Recipient
        exclude = ["owner"]

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
        })
        self.fields["full_name"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["comment"].widget.attrs.update({
            "class": "form-control",
            "rows": 3,
        })


class MessageForm(forms.ModelForm):

    class Meta:

        model = Message
        exclude = ["owner"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update({
            "class": "form-control",
        })
        self.fields["content"].widget.attrs.update({
            "class": "form-control",
            "rows": 3,
        })