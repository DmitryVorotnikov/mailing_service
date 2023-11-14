from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import MailingLog


def set_mailing_affiliation(mailing):
    """
    Явно задает у клиентов в поле mailings_list принадлежность к рассылке.
    """
    for client in mailing.clients_list.all():
        if not client.mailings_list.filter(pk=mailing.pk).exists():
            client.mailings_list.add(mailing)


def send_mail_make_report(mailing):
    """
    Отправляет письмо и формируем отчет.
    """
    # Проверяем что рассылка запущена.
    if mailing.status == 'started':

        # Переменные для формирования отчета объявляем до цикла.
        clients_full_name_list = []
        clients_email_list = []
        status = MailingLog.STATUS_OK
        error_message = []

        # Запускаем цикл по каждому клиенту.
        for client in mailing.clients_list.all():
            clients_full_name_list.append(client.full_name)
            clients_email_list.append(client.email)

            # Отправляем письмо
            try:
                send_mail(
                    subject=mailing.send_mail_subject,
                    message=mailing.send_mail_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

            except SMTPException as e:
                status = MailingLog.STATUS_FAILED
                error_message.append(str(e))

        # Удаляем старый отчет если он существует.
        existing_log = MailingLog.objects.filter(mailing=mailing)
        if existing_log.exists():
            existing_log.delete()

        # Создаем отчет - объект класса MailingLog.
        MailingLog.objects.create(
            mailing=mailing,
            last_mailing=timezone.now(),
            status=status,
            clients_full_name=clients_full_name_list,
            clients_email=clients_email_list,
            mailing_name=mailing.mailing_name,
            error_message=error_message
        )
