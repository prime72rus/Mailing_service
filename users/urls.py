from django.urls import path
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from users.views import (
    RegisterView,
    RegisterUpdateView,
    BlockedUserView,
    email_verification,
    UserListView,
)
from users.forms import CustomLoginForm

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html", form_class=CustomLoginForm
        ),
        name="login",
    ),
    path(
        "logout/", LogoutView.as_view(next_page="mailing:index"), name="logout"
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "user_profile/<int:pk>/update/",
        RegisterUpdateView.as_view(),
        name="user_profile_update",
    ),
    path(
        "email-confirm/<str:token>/", email_verification, name="email_confirm"
    ),
    path(
        "blocked/user/<int:pk>/",
        BlockedUserView.as_view(),
        name="blocked_user",
    ),
    path("users_list/", cache_page(60 * 2)(UserListView.as_view()), name="users_list"),


    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
            subject_template_name="registration/password_reset_subject.txt"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete")),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
