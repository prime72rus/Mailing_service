from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView
from users.forms import (
    UserRegisterForm,
    UserProfileUpdateForm,
    UserManagerForm,
)
from users.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.core.exceptions import PermissionDenied
from users.services import send_verification_email, verify_user_email


class RegisterView(FormView):

    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):

        user = form.save()
        user.is_active = False
        user.save()
        send_verification_email(user, self.request)
        return super().form_valid(form)


def email_verification(request, token):
    return verify_user_email(token)


class RegisterUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    template_name = "users/user_profile_update.html"
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy("mailing:index")


class BlockedUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = User
    template_name = "users/blocked_user.html"
    form_class = UserManagerForm
    success_url = reverse_lazy("users:users_list")

    def test_func(self):

        user_to_block = self.get_object()
        current_user = self.request.user

        if not current_user.has_perm("users.can_blocked_user"):
            return False

        if current_user == user_to_block:
            raise PermissionDenied("Вы не можете блокировать себя")

        if user_to_block.is_superuser and not current_user.is_superuser:
            raise PermissionDenied(
                "Только суперпользователь может "
                "блокировать других суперпользователей"
            )

        return True

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(
                "У вас нет прав для блокировки пользователей"
            )
        return super().handle_no_permission()


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = "users.can_blocked_user"
    template_name = "users/users_list.html"
    context_object_name = "users"
