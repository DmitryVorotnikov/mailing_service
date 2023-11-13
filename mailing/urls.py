from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='clients_list'),
    path('create/', ClientCreateView.as_view(), name='clients_create'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='clients_edit'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='clients_delete'),
]