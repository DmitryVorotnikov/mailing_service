from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, MailingListView, \
    MailingCreateView, MailingUpdateView, MailingDeleteView, MailingLogListView, MainListView

app_name = MailingConfig.name

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view(), name='clients_edit'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='clients_delete'),

    path('mailings/', MailingListView.as_view(), name='mailings_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailings_create'),
    path('mailings/edit/<int:pk>/', MailingUpdateView.as_view(), name='mailings_edit'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailings_delete'),

    path('report/', MailingLogListView.as_view(), name='report_list'),


    path('', MainListView.as_view(), name='main_page'),
]
