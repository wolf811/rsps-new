from django.db import models
from mainapp.models import Conference

# Create your models here.
class ConferenceTheme(models.Model):
    subject = models.CharField(u'Вопрос повестки дня', max_length=200)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Вопрос повестки дня'
        verbose_name_plural = 'Вопросы повестки дня'