from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User


class UserRegisterForm(UserCreationForm):

    usable_password = None

    class Meta:

        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите свой Email",
            }
        )
        self.fields["email"].help_text = None

        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите имя",
            }
        )
        self.fields["first_name"].label = "Ваше имя"

        self.fields["last_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите фамилию",
            }
        )
        self.fields["last_name"].label = "Ваша фамилия"

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите пароль",
            }
        )
        self.fields["password1"].label = "Пароль:"

        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторите ввод пароля",
            }
        )
        self.fields["password2"].label = "Подтверждение пароля:"


class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )
        self.fields["password"].label = "Пароль"


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = User
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите имя",
            }
        )
        self.fields["first_name"].label = "Ваше имя"

        self.fields["last_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите фамилию",
            }
        )
        self.fields["last_name"].label = "Ваша фамилия"


class UserManagerForm(forms.ModelForm):

    class Meta:

        model = User
        fields = ["email", "is_active"]

    def __init__(self, *args, **kwargs):
        super(UserManagerForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите название продукта",
            }
        )
        self.fields["email"].label = ""
        self.fields["email"].disabled = True
        self.fields["is_active"].label = "Снимите флаг для блокировки"
        self.fields["is_active"].help_text = ""
        self.fields["is_active"].widget = forms.CheckboxInput(
            attrs={
                "class": "form-check-input toggle-switch",
                "role": "switch",
                "id": "is_active_switch",
            }
        )
