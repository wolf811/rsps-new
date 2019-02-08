"""rsps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import mainapp.views as mainapp
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.index, name = 'index'),
    path('contact/', mainapp.contact, name = 'contact'),
    path('account/', mainapp.account, name = 'account'),
    path('registration/', mainapp.registration, name = 'registration'),
    path('about/', mainapp.about, name = 'about'),
    path('news/', mainapp.news, name = 'news'),
    path('docs/', mainapp.docs, name = 'docs'),
    path('regionalOffice/', mainapp.regionalOffice, name = 'regionalOffice'),
    path('conf/', mainapp.conf, name = 'conf'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
