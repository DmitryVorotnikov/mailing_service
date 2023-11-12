from django.db import models

# Create your models here.
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

