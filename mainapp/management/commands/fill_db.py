from django.core.management.base import BaseCommand
from django.urls import reverse
from django.core.files import File
from mainapp.models import Post, Member, Conference, Photo
# from django.conf import settings
from mixer.backend.django import mixer
import random
# from model_mommy.recipe import Recipe, foreign_key, seq

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

class Command(BaseCommand):
    def handle(self, *args, **options):
        #delete all
        Post.objects.all().delete()
        Photo.objects.all().delete()
        Member.objects.all().delete()
        Conference.objects.all().delete()

        #make PostPhotos
        for i in range(0, len(images)):
            #make Tags
            mixer.blend(Member),
            mixer.blend(Conference)
            #make Posts without pictures
            mixer.blend(Post, title=random.choice(news_titles))
            mixer.blend(Photo, image=File(open(images[i], 'rb')))

        for conference in Conference.objects.all():
            conference.members.add(Member.objects.first())

        print('*********fill_db_complete************')