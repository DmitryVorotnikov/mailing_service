import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, RedirectView, ListView
from users.forms import UserRegisterForm, UserProfileForm, UserForManagerForm

from config import settings
from users.models import User


class LogoutUserView(LoginRequiredMixin, LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('mailing:main_page')

    def form_valid(self, form):
        # Сохранение в оперативную память (без добавление в БД).
        user = form.save(commit=False)
        # Пользователь неактивен, пока не подтвердит email.
        user.is_active = False
        # Генерируем токен, через secrets, и сохраняет его в поле пользователя.
        user.confirmation_token = secrets.token_urlsafe(30)
        user.save()

        # Создаем ссылку с токеном на следующий контроллер-представление.
        verification_link = self.request.build_absolute_uri(
            reverse_lazy('users:verify_email', kwargs={'token': user.confirmation_token}),
        )

        # Отправляем письмо с ссылкой-токеном.
        send_mail(
            subject='Верификация аккаунта',
            message=f'Осталось только подтвердить ваш аккаунт, перейдя по ссылке: {verification_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class VerifyEmailView(RedirectView):
    # Устанавливает перенаправление как временное (а не постоянное).
    permanent = False
    # Устанавливает сохранение параметров запроса и включение их в целевой URL после перенаправления.
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        # Получает токен из URL.
        token = kwargs.get('token')
        try:
            # Ищет по токену пользователя с таким же токеном.
            user = User.objects.get(confirmation_token=token)
            # Активация пользователя.
            user.is_active = True
            # Удаление токена из поля пользователя (опционально).
            user.confirmation_token = ''
            user.save()
            return reverse('users:login')
        except User.DoesNotExist:
            print('Неверный токен')
            # Если токен неверный или истек, можно перенаправить на страницу с ошибкой.
            return reverse('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailing:main_page')

    # Что бы не пришлось на страницу профиля передавать pk.
    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()

        # Если пользователь is_staff=True, то показываем всех обычных пользователей.
        if self.request.user.is_staff:
            return queryset.exclude(is_staff=True)
        # Если пользователь is_staff=False, то вызываем ошибку.
        else:
            raise Http404


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForManagerForm
    success_url = reverse_lazy('users:users_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Если пользователь is_staff=True, то доступ разрешен к редактированию обычных пользователя.
        if self.request.user.is_staff and not self.object.is_staff:
            return self.object
        else:
            raise Http404('Доступ запрещен')
