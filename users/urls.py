from django.urls import path
# from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView
from users.views import RegisterView, RegisterUpdateView, BlockedUserView, email_verification, UserListView
from users.forms import CustomLoginForm


app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html", form_class=CustomLoginForm), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailing:index"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("user_profile/<int:pk>/update/", RegisterUpdateView.as_view(), name="user_profile_update"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
    path("blocked/user/<int:pk>/", BlockedUserView.as_view(), name="blocked_user"),
    path("users_list/", UserListView.as_view(), name="users_list"),
]