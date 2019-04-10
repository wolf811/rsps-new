from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def textvalidation(value):
    template = re.compile('^[a-zA-Zа-яА-Я\s]+')
    m = template.match(value)
    if not m:
        error_text = '{} недопустимое значение поля ФИО'.format(value)
        raise ValidationError({
            'fio': ValidationError(error_text, code='invalid'),
        })


# Create your models here.
class Member(models.Model):
    """docstring for Member"""
    fio = models.CharField(db_index=True, max_length=100, verbose_name='ФИО')
    job = models.CharField(db_index=True, max_length=100, verbose_name='Место работы')
    jobplace = models.CharField(db_index=True, max_length=100, verbose_name='Должность')
    tel = models.CharField(max_length=100, verbose_name='Телефон')
    email = models.EmailField(max_length=100, verbose_name='Email')
    city = models.CharField(max_length=100, verbose_name='Город проживания')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    short_description = models.TextField(u'Краткая информация (награды, звания и т.д.)',
                                            blank=True, null=True, default=None)
    subscription = models.BooleanField(u'Подписка на обновления')
    # membership = models.BooleanField(verbose_name='Членство в РСПС')
    # conference = models.ForeignKey(Conference, verbose_name='Зареристрирован на:',
    # 	default=null, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return '{}, {}'.format(self.fio, self.job)

    def clean(self):
        textvalidation(self.fio)

class Post(models.Model):
    """model for publications"""
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, verbose_name='Название публикации')
    short_description = models.CharField(max_length=200, verbose_name='Краткое описание', blank=True, default='')
    text = RichTextUploadingField(verbose_name='Текст публикации')
    published_date = models.DateTimeField(u'Дата публикации', default=timezone.now)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return 'Публикация {}, дата {}'.format(self.title, self.published_date)

class Conference(models.Model):
    """docstring for Conference"""
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, verbose_name='Название конференции')
    date = models.DateField(verbose_name='Дата проведения')
    place = models.CharField(max_length=100, verbose_name='Место проведения')
    completed = models.BooleanField(verbose_name='Проведена', default=False)
    members = models.ManyToManyField(Member, verbose_name='Участники', blank=True, default=None)
    publication = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Конференция'
        verbose_name_plural = 'Конференции'

    def __str__(self):
        return '{}, {}'.format(self.title, self.date)




class Photo(models.Model):
    """model for handling photos"""
    image = models.ImageField(u'Фото', upload_to='upload/')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)