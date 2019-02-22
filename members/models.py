from django.db import models
from mainapp.models import Member
# Create your models here.


class Membership(models.Model):
    STATUS_CHOICES = (
        ('Новый', 'Новый член РСПС'),
        ('Заявлен', 'Заявлен на утверждение Президиумом РСПС'),
        ('Одобрен', 'Утвержден Президиумом РСПС'),
        ('Выдан сертификат', 'Выдан сертификат РСПС'),
    )
    member = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='Новый')

    class Meta:
        verbose_name = 'статус членства'
        verbose_name_plural = 'статусы членства'
