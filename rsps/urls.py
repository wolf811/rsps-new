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
    path('user/', mainapp.user, name = 'user'),
    path('account_user/', mainapp.account_user, name = 'account_user'),
    path('account_about/', mainapp.account_about, name = 'account_about'),
    path('account_news/', mainapp.account_news, name = 'account_news'),
    path('account_employee/', mainapp.account_employee, name = 'account_employee'),
    path('account_conf/', mainapp.account_conf, name = 'account_conf'),
    path('registration/', mainapp.registration, name = 'registration'),
    path('about/', mainapp.about, name = 'about'),
    path('news/', mainapp.news, name = 'news'),
    path('docs/', mainapp.docs, name = 'docs'),
    path('regional_office/', mainapp.regional_office, name = 'regional_office'),
    path('regional_office_detail/', mainapp.regional_office_detail, name = 'regional_office_detail'),
    path('reestr/', mainapp.reestr, name = 'reestr'),
    path('conf/', mainapp.conf, name = 'conf'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
