from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    mailings_list = models.ManyToManyField('Mailing', blank=True, related_name='clients', verbose_name='Рассылка')
    email = models.EmailField(verbose_name='email клиента')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.TextField(max_length=300, verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('id',)


class Mailing(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'
    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_STARTED, 'Запущена'),
        (STATUS_CREATED, 'Создана'),
        (STATUS_DONE, 'Завершена'),
    )

    clients_list = models.ManyToManyField('Client', blank=True, related_name='mailings', verbose_name='Клиент')
    mailing_name = models.CharField(max_length=200, verbose_name='Имя рассылки')
    time = models.TimeField(verbose_name='Время рассылки')
    period = models.CharField(max_length=25, choices=PERIODS, verbose_name='Периодичность')
    status = models.CharField(max_length=25, choices=STATUSES, verbose_name='Статус')
    send_mail_subject = models.CharField(max_length=200, verbose_name='Тема письма')
    send_mail_message = models.TextField(max_length=1500, verbose_name='Текст письма')

    def __str__(self):
        return f'{self.mailing_name}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('id',)


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='Рассылка')
    last_mailing = models.DateTimeField(verbose_name='Время последней попытки')
    status = models.CharField(max_length=25, choices=STATUSES, verbose_name='Статус')
    clients_full_name = models.TextField(verbose_name='ФИО клиентов')
    clients_email = models.TextField(verbose_name='email клиентов')
    mailing_name = models.CharField(max_length=200, verbose_name='Имя рассылки')
    error_message = models.TextField(verbose_name='Сообщение об ошибке', **NULLABLE)

    def __str__(self):
        return f'{self.mailing_name} - {self.last_mailing}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
        ordering = ('id',)
