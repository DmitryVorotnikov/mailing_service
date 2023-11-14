from mailing.models import Mailing
from mailing.services import send_mail_make_report


def send_mail_make_report_for_all():
    """
    Функция выполнить отправку писем и создание отчетов по каждой запущенной рассылке.
    """
    print('Hellow')
