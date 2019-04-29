from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension, FileExtensionValidator
import re
import hashlib


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

def file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Файл слишком велик, размер файла не должен превышать 2mb')


class Photo(models.Model):
    """model for handling photos"""
    image = models.ImageField(u'Фото', upload_to='upload/')
        # validators=[FileExtensionValidator(['jpg', 'JPG', 'png', 'PNG']), file_size])
        # validators=[validate_image_file_extension, file_size])
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    file_sha1 = models.CharField(max_length=40, unique=True)
    filesize = models.CharField(max_length=40)

    def clean(self):
        file_size(self.image)
        validate_image_file_extension(self.image)
        return True

    def __str__(self):
        return self.image.url

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        f = self.image.file.open('rb')
        hash = hashlib.sha1()
        if f.multiple_chunks():
            for chunk in f.chunks():
                hash.update(chunk)
        else:
                hash.update(f.read())
        f.close()
        self.file_sha1 = hash.hexdigest()
        self.filesize = self.image.size
        #call the real save()
        super(Photo, self).save(*args, **kwargs)
        # models.Model.save(self, *args, **kwargs)
        # import pdb; pdb.set_trace()