from django.contrib import admin
from mailing.models import Client, Mailing, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name',)
    search_fields = ('email', 'full_name',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_name', 'time', 'period', 'status', 'send_mail_subject', 'send_mail_message',)
    list_filter = ('status',)
    search_fields = ('mailing_name',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_mailing', 'status', 'clients_full_name', 'clients_email', 'mailing_name', 'error_message',)
    list_filter = ('status',)
    search_fields = ('mailing_name',)
