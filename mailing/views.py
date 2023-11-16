from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Article
from mailing.forms import ClientForm, MailingForUserForm, MailingForManagerForm
from mailing.models import Client, Mailing, MailingLog
from mailing.services import set_mailing_affiliation, send_mail_make_report


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()

        # Если пользователь is_staff=True и is_superuser=False, то вызываем ошибку.
        if self.request.user.is_staff and not self.request.user.is_superuser:
            raise Http404('Доступ запрещен')
        # Если пользователь админ, то показываем всех клиентов.
        elif self.request.user.is_superuser:
            return queryset
        # Если обычный пользователь, то показываем только его клиентов.
        else:
            return queryset.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')

    def dispatch(self, request, *args, **kwargs):
        # Если пользователь is_staff=True и is_superuser=False, то вызываем ошибку.
        if request.user.is_staff and not request.user.is_superuser:
            raise Http404('Доступ запрещен')
        # Если пользователь админ или обычный пользователь, то доступ разрешен.
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()

        # Присваиваем в качестве владельца текущего пользователя.
        self.object.owner = self.request.user
        self.object = form.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Если пользователь is_staff=True и is_superuser=False, то вызываем ошибку.
        if self.request.user.is_staff and not self.request.user.is_superuser:
            raise Http404('Доступ запрещен')
        # Если пользователь админ, то доступ разрешен к редактированию всех клиентов.
        elif self.request.user.is_superuser:
            return self.object
        # Если обычный пользователь, то доступ разрешен к редактированию только его клиентов.
        elif self.object.owner == self.request.user:
            return self.object
        else:
            raise Http404('Доступ запрещен')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Если пользователь is_staff=True и is_superuser=False, то вызываем ошибку.
        if self.request.user.is_staff and not self.request.user.is_superuser:
            raise Http404('Доступ запрещен')
        # Если пользователь админ, то доступ разрешен к удалению всех клиентов.
        elif self.request.user.is_superuser:
            return self.object
        # Если обычный пользователь, то доступ разрешен к удалению только его клиентов.
        elif self.object.owner == self.request.user:
            return self.object
        else:
            raise Http404('Доступ запрещен')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()

        # Если пользователь is_staff=True или is_superuser=True, то показываем все рассылки.
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        # Если обычный пользователь, то показываем только его рассылки.
        else:
            return queryset.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForUserForm
    success_url = reverse_lazy('mailing:mailings_list')

    def dispatch(self, request, *args, **kwargs):
        # Если пользователь is_staff=True и is_superuser=False, то вызываем ошибку.
        if request.user.is_staff and not request.user.is_superuser:
            raise Http404('Доступ запрещен')
        # Если пользователь админ или обычный пользователь, то доступ разрешен.
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()

        # Присваиваем в качестве владельца текущего пользователя.
        self.object.owner = self.request.user
        self.object = form.save()

        # Явно задает у клиентов в поле mailings_list принадлежность (или ее отсутствие) к рассылке.
        set_mailing_affiliation(self.object)
        # Отправляем письмо и формируем отчет.
        send_mail_make_report(self.object, self.request.user)  #######################################
        # send_mail_make_report_for_all()

        return super().form_valid(form)

    # Передаем текущего пользователя в качестве аргумента в формы, чтобы в списке clients_list можно
    # было выбирать только клиентов текущего пользователя.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Если пользователь админ, то ему доступен выбор всех клиентов всех пользователей.
        if self.request.user.is_superuser:
            return kwargs
        # Если обычный пользователь, то ему доступен выбор только своих клиентов.
        else:
            kwargs['user'] = self.request.user
            return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForUserForm
    success_url = reverse_lazy('mailing:mailings_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Если пользователь is_staff=True или is_superuser=True, то разрешен доступ к редактированию всех рассылок.
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.object
        # Если обычный пользователь, то доступ разрешен к редактированию только его рассылок.
        elif self.object.owner == self.request.user:
            return self.object
        else:
            raise Http404('Доступ запрещен')

    def get_form_class(self, *args, **kwargs):
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            # Вернуть форму MailingForUserForm для владельца рассылки или админа.
            return MailingForUserForm
        elif self.request.user.is_staff:
            # Вернуть форму MailingForManagerForm для пользователя с is_staff=True.
            return MailingForManagerForm
        else:
            # Вызвать 404 ошибку если ни одно условие не подошло.
            raise Http404

    def form_valid(self, form):
        self.object = form.save()

        # Явно задает у клиентов в поле mailings_list принадлежность (или ее отсутствие) к рассылке.
        set_mailing_affiliation(self.object)
        # Отправляем письмо и формируем отчет.
        send_mail_make_report(self.object, self.request.user)  #######################################
        # send_mail_make_report_for_all()

        return super().form_valid(form)

    # Передаем текущего пользователя в качестве аргумента в формы, чтобы в списке clients_list можно
    # было выбирать только клиентов текущего пользователя.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Обычному пользователю доступен выбор только собственных клиентов для clients_list.
        if self.request.user.is_superuser or self.request.user.is_staff:
            return kwargs
        else:
            kwargs['user'] = self.request.user
            return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailings_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Если пользователь is_staff=True и is_superuser=False, то вызываем ошибку.
        if self.request.user.is_staff and not self.request.user.is_superuser:
            raise Http404('Доступ запрещен')
        # Если пользователь админ, то доступ разрешен к удалению всех рассылок.
        elif self.request.user.is_superuser:
            return self.object
        # Если обычный пользователь, то доступ разрешен к удалению только его рассылок.
        elif self.object.owner == self.request.user:
            return self.object
        else:
            raise Http404('Доступ запрещен')


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog

    def get_queryset(self):
        queryset = super().get_queryset()

        # Если пользователь is_staff=True и is_superuser=False, то вызываем ошибку.
        if self.request.user.is_staff and not self.request.user.is_superuser:
            raise Http404('Доступ запрещен')
        # Если пользователь админ, то показываем все отчеты.
        elif self.request.user.is_superuser:
            return queryset
        # Если обычный пользователь, то показываем только его отчеты.
        else:
            return queryset.filter(owner=self.request.user)


class MainListView(ListView):
    model = Article
    template_name = 'mailing/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все объекты Article и берем только последние четыре
        context['object_list'] = Article.objects.all().order_by('-id')[:4]

        # Добавляем данные для отображения на главной странице
        context['mailing_count'] = Mailing.objects.count()
        context['mailing_active_count'] = Mailing.objects.filter(status='started').count()
        context['client_count'] = Client.objects.count()

        return context
