from django.contrib.auth.views import LoginView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, VerifyEmailView, LogoutUserView, UserListView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify_email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),

    path('users_list/', UserListView.as_view(), name='users_list'),
    path('users_list/edit/<int:pk>/', UserUpdateView.as_view(), name='users_edit'),
]
