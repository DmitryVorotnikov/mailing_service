from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MailingForm
from mailing.models import Client, Mailing, MailingLog
from mailing.services import set_mailing_affiliation, send_mail_make_report


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients_list')


class MailingListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings_list')

    def form_valid(self, form):
        self.object = form.save()

        # Явно задаем у клиентов в поле mailings_list принадлежность к рассылке.
        set_mailing_affiliation(self.object)
        # Отправляем письмо и формируем отчет.
        send_mail_make_report(self.object)

        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings_list')

    def form_valid(self, form):
        self.object = form.save()

        # Явно задаем у клиентов в поле mailings_list принадлежность к рассылке.
        set_mailing_affiliation(self.object)
        # Отправляем письмо и формируем отчет.
        send_mail_make_report(self.object)

        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailings_list')


class MailingLogListView(ListView):
    model = MailingLog
