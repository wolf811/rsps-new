from django.db import models
from mainapp.models import Member
# Create your models here.

STATUS_CHOICES = (
    ('Новый', 'Новый член РСПС'),
    ('Заявлен', 'Заявлен на утверждение Президиумом РСПС'),
    ('Одобрен', 'Утвержден Президиумом РСПС'),
    ('Выдан сертификат', 'Выдан сертификат РСПС'),
)

class Membership(models.Model):
    member = models.OneToOneField(Member, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='Новый')

    class Meta:
        verbose_name = 'статус членства'
        verbose_name_plural = 'статусы членства'

    def __str__(self):
        return self.status


class MemberRegistration(models.Model):
    """registration to something with name and related to member"""
    member = models.ForeignKey(Member, null=True, blank=True, default=None,
                               on_delete=models.SET_NULL)
    name = models.CharField(u'Название регистрации', max_length=150)
    register = models.NullBooleanField(u'Зарегистрировать')
