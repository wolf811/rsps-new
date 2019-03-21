from django.core.management.base import BaseCommand
from django.urls import reverse
from django.core.files import File
from mainapp.models import Post, Member, Conference, Photo
from members.models import Membership
from django.contrib.auth.models import User
# from django.conf import settings
from mixer.backend.django import mixer
import random


# from model_mommy.recipe import Recipe, foreign_key, seq

try:
    popov_user = User.objects.get(username='popov')
except:
    popov_user=User.objects.create(username='popov', email='popov@naks.ru', password='2011')

images = [
    'media/01.JPG',
    'media/02.JPG',
    'media/03.JPG',
    'media/04.JPG',
    'media/05.JPG',
    'media/06.JPG',
]

news_titles = [
    'Конференция НАКС',
    'Общее собрание',
    'Семинар НАКС',
    'Вебинар НАКС',
]

names = ['Иван', 'Сергей', 'Владимир', 'Александр', 'Валентин', 'Анатолий', 'Кирилл']
second_names = ['Иванович', 'Сергеевич', 'Владимирович', 'Александрович', 'Валентинович', 'Анатольевич', 'Кириллович']
last_names = ['Иванов', 'Пономаренко', 'Минаев', 'Гончаров', 'Комбаров', 'Попов', 'Кузнецов']

job_places = ['Сварка трубопроводов', 'ООО Аттестационный центр', 'Сибирские трубомагистрали', 'Транснефть', 'Мегионгазсервис', 'Нижневартовскгоргаз']

jobs = ['Главный сварщик', 'Инженер', 'Сварщик', 'Главный инженер', 'Слесарь', 'Контролер сварочных работ']

class Command(BaseCommand):
    def handle(self, *args, **options):
        #delete all
        Post.objects.all().delete()
        Photo.objects.all().delete()
        Member.objects.all().delete()
        Membership.objects.all().delete()
        Conference.objects.all().delete()

        #make PostPhotos
        for i in range(0, len(images)):
            #make Tags
            #make Posts without pictures
            mixer.blend(Post, title=random.choice(news_titles))
            mixer.blend(Photo, image=File(open(images[i], 'rb')))
        for i in range(20):
            mixer.blend(Member, fio='{} {} {}'.format(
                random.choice(last_names),
                random.choice(names),
                random.choice(second_names)),
                job=random.choice(job_places),
                jobplace=random.choice(jobs),
                tel=lambda: '8(925){}-{}-{}'.format(random.randint(100, 999),
                                                    random.randint(10, 99),
                                                    random.randint(10, 99)),
                user=popov_user
            )
        for i in range (0, 20):
            mixer.blend(Conference, user=popov_user)
        for conference in Conference.objects.all():
            conference.members.add(Member.objects.first())

        print('*********fill_db_complete************')