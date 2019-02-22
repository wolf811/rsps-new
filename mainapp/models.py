from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# Create your models here.
class Member(models.Model):
    """docstring for Member"""
    fio = models.CharField(max_length=100, verbose_name='ФИО')
    job = models.CharField(max_length=100, verbose_name='Место работы')
    jobplace = models.CharField(max_length=100, verbose_name='Должность')
    tel = models.CharField(max_length=100, verbose_name='Телефон')
    email = models.CharField(max_length=100, verbose_name='Email')
    membership = models.BooleanField(verbose_name='Членство в РСПС')
    # conference = models.ForeignKey(Conference, verbose_name='Зареристрирован на:', 
    # 	default=null, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return '{}, {}'.format(self.fio, self.job)

class Conference(models.Model):
    """docstring for Conference"""
    title = models.CharField(max_length=200, verbose_name='Название конференции')
    date = models.DateField(verbose_name='Дата проведения')
    place = models.CharField(max_length=100, verbose_name='Место проведения')
    completed = models.BooleanField(verbose_name='Проведена')
    members = models.ManyToManyField(Member, verbose_name='Участники')

    class Meta:
        verbose_name = 'Конференция'
        verbose_name_plural = 'Конференции'

    def __str__(self):
        return '{}, {}'.format(self.title, self.date)

class Post(models.Model):
    """model for publications"""
    title = models.CharField(max_length=200, verbose_name='Название публикации')
    short_description = models.CharField(max_length=100, verbose_name='Краткое описание', blank=True, default='')
    text = RichTextUploadingField(verbose_name='Текст публикации')
    published_date = models.DateTimeField(u'Дата публикации', default=timezone.now)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return 'Публикация {}, дата {}'.format(self.title, self.published_date)

class Photo(models.Model):
    """model for handling photos"""
    image = models.ImageField(u'Фото', upload_to='upload/')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)