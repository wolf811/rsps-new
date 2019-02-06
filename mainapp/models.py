from django.db import models

# Create your models here.
class Conference(models.Model):
	"""docstring for Conference"""
	title = models.CharField(max_length=200, verbose_name='Название конференции')
	date = models.DateField(verbose_name='Дата проведения')
	place = models.CharField(max_length=100, verbose_name='Место проведения')
	completed = models.BooleanField(verbose_name='Проведена')

	class Meta:
		verbose_name = 'Конференция'
		verbose_name_plural = 'Конференции'

	def __str__(self):
		return '{}-{}'.format(self.title, self.date)

class Member(models.Model):
	"""docstring for Member"""
	fio = models.CharField(max_length=100, verbose_name='ФИО')
	job = models.CharField(max_length=100, verbose_name='Место работы')
	jobplace = models.CharField(max_length=100, verbose_name='Должность')
	tel = models.CharField(max_length=100, verbose_name='Телефон')
	email = models.CharField(max_length=100, verbose_name='Email')
	membership = models.BooleanField(verbose_name='Членство в РСПС')

	class Meta:
		verbose_name = 'Участник'
		verbose_name_plural = 'Участники'

	def __str__(self):
		return '{}-{}'.format(self.title, self.date)