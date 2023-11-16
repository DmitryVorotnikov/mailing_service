from django import forms

from mailing.models import Client, Mailing


class StyleFormMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment',)


class MailingForUserForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('clients_list', 'mailing_name', 'time', 'period', 'status', 'send_mail_subject', 'send_mail_message',)

    def __init__(self, *args, **kwargs):
        # Получаем текущего пользователя из аргументов формы.
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Фильтруем клиентов, принадлежащих текущему пользователю.
            self.fields['clients_list'].queryset = Client.objects.filter(owner=user)
        else:
            # Если user = None, значит текущий пользователь это админ, ему доступен список всех клиентов.
            self.fields['clients_list'].queryset = Client.objects.all()


class MailingForManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('status', 'send_mail_subject', 'send_mail_message',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если пользователь is_staff=True, то он может редактировать
        # только поле 'status', остальные поля только для чтения.
        self.fields['send_mail_subject'].widget.attrs['readonly'] = True
        self.fields['send_mail_message'].widget.attrs['readonly'] = True

