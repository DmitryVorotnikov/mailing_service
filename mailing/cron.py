from datetime import datetime, timedelta

from django.utils import timezone

from mailing.models import Mailing, MailingLog
from mailing.services import send_mail_make_report


def send_mail_make_report_for_all():
    """
    Функция проверит созданные отчеты, время рассылки и текущее время и на основе этих данных
    может выполнить отправку писем и создание отчетов по каждой запущенной рассылке.
    """
    # Получаем QuerySet всех рассылок.
    mailing_list = Mailing.objects.all()

    # Получаем текущее datetime и time.
    datetime_now = timezone.localtime(timezone.now())  # datetime
    time_now = datetime_now.time()  # time

    for mailing in mailing_list:
        # Получаем владельца рассылки.
        mailing_owner = mailing.owner

        # Получаем time указанный в настройках рассылки.
        time_mailing = mailing.time  # time

        # Получаем отчет для выбранной в цикле рассылки.
        mailing_log = MailingLog.objects.get(mailing=mailing)
        # Получаем datetime и time последний рассылки из отчета.
        datetime_last_mailing = mailing_log.last_mailing  # datetime
        time_last_mailing = datetime_last_mailing.time()  # time

        if mailing_log and mailing.period == 'daily' and mailing.status == 'started':
            # Проверяем, находится ли время рассылки в диапазоне часа от времени последней рассылки.
            if abs(time_mailing.hour - time_last_mailing.hour) <= 1:
                print('Письмо уже было отправлено недавно')
            # Проверяем, находится ли текущее время в диапазоне часа от времени рассылки.
            elif abs(time_mailing.hour - time_now.hour) <= 1:
                print('Текущее время в пределах часа, надо отправлять письмо и создавать отчет')
                send_mail_make_report(mailing, mailing_owner)
            else:
                print('Текущее время не в пределах часа, ничего не делаем')

        if mailing_log and mailing.period == 'weekly' and mailing.status == 'started':
            # Рассылка "Раз в неделю" будет происходить в указанное время, в понедельник текущей недели.
            # Определяем разницу в днях между текущим днем недели и понедельником.
            days_until_monday = (datetime_now.weekday() - 0) % 7

            # Создаем новый объект datetime с понедельником текущей недели и тем же указанным временем рассылки.
            monday_time_mailing = datetime.combine(datetime_now - timedelta(days=days_until_monday), time_mailing)

            # Добавляем в monday_time_mailing данные по часовому поясу чтобы объект можно было сравнивать.
            monday_time_mailing_tz = monday_time_mailing.replace(tzinfo=datetime_last_mailing.tzinfo)

            # Проверка, находится ли monday_time_mailing_tz в пределах часа от time_last_mailing.
            if datetime_last_mailing - timedelta(
                    hours=1) <= monday_time_mailing_tz <= datetime_last_mailing + timedelta(
                hours=1):
                print('Письмо уже было отправлено недавно')
            # Проверка, находится ли monday_time_mailing_tz в пределах часа от datetime_now.
            elif datetime_now - timedelta(hours=1) <= monday_time_mailing_tz <= datetime_now + timedelta(
                    hours=1):
                print('Текущее время в пределах часа, надо отправлять письмо и создавать отчет')
                send_mail_make_report(mailing, mailing_owner)
            else:
                print('Текущее время не в пределах часа, ничего не делаем')

        if mailing_log and mailing.period == 'monthly' and mailing.status == 'started':
            # Рассылка "Раз в месяц" будет происходить в указанное время, в первое число текущего месяца.
            # Создаем новый объект datetime с первым числом текущего месяца и временем из time_mailing
            first_day_time_mailing = datetime(datetime_now.year, datetime_now.month, 1, time_mailing.hour,
                                              time_mailing.minute,
                                              time_mailing.second)

            # Добавляем в first_day_time_mailing данные по часовому поясу чтобы объект можно было сравнивать.
            first_day_time_mailing_tz = first_day_time_mailing.replace(tzinfo=datetime_last_mailing.tzinfo)

            # Проверка, находится ли first_day_time_mailing_tz в пределах часа от time_last_mailing.
            if datetime_last_mailing - timedelta(
                    hours=1) <= first_day_time_mailing_tz <= datetime_last_mailing + timedelta(hours=1):
                print('Письмо уже было отправлено недавно')
            # Проверка, находится ли first_day_time_mailing_tz в пределах часа от datetime_now.
            elif datetime_now - timedelta(hours=1) <= first_day_time_mailing_tz <= datetime_now + timedelta(
                    hours=1):
                print('Текущее время в пределах часа, надо отправлять письмо и создавать отчет')
                send_mail_make_report(mailing, mailing_owner)
            else:
                print('Текущее время не в пределах часа, ничего не делаем')

        if not mailing_log and mailing.status == 'started':
            print('Отчет еще не был создан, надо отправлять письмо и создавать отчет')
            send_mail_make_report(mailing, mailing_owner)
