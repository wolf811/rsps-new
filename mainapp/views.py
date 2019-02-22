from django.shortcuts import render
from mainapp.models import Conference, Post
from mainapp.models import Member, Photo
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    title = 'РСПС - Главная'
    content = {
        'title': title
    }
    return render(request, 'mainapp/index.html', content)

def contact(request):
    title = 'РСПС - Контакты'
    content = {
        'title': title
    }
    return render(request, 'mainapp/contact.html', content)

def user(request):
    title = 'РСПС - Личный кабинет'
    content = {
        'title': title, 
    }
    return render(request, 'mainapp/user.html', content)

def account_user(request):
    title = 'РСПС - Личный кабинет'
    content = {
        'title': title, 
    }
    return render(request, 'mainapp/account_user.html', content)
    
def account_about(request):
    title = 'РСПС - Личный кабинет'
    content = {
        'title': title, 
    }
    return render(request, 'mainapp/account_about.html', content)

def account_news(request):
    title = 'РСПС - Личный кабинет'
    content = {
        'title': title, 
    }
    return render(request, 'mainapp/account_news.html', content)

def account_conf(request):
    title = 'РСПС - Личный кабинет'
    conferences = Conference.objects.all()
    # members = Member.objects.all()
    content = {
        'title': title, 
        'conferences': conferences,
        # 'members': members,
    }
    return render(request, 'mainapp/account_conf.html', content)

def account_employee(request):
    title = 'РСПС - Личный кабинет'
    # employee = Employee.objects.all()
    content = {
        'title': title, 
        # 'employee': employee,
    }
    return render(request, 'mainapp/account_employee.html', content)

def registration(request):
    title = 'РСПС - Регистрация'
    content = {
        'title': title
    }
    return render(request, 'mainapp/registration.html', content)

def about(request):
    title = 'РСПС - О РСПС'
    content = {
        'title': title
    }
    return render(request, 'mainapp/about.html', content)

def news(request):
    title = 'РСПС - Новости'
    news_page_posts = []
    all_posts = Post.objects.all()
    for post in all_posts:
        photo = Photo.objects.filter(post__pk=post.pk).first()
        news_page_posts.append(
            {'post': post, 'photo': photo, }
        )
    # for publication in news_page_posts:
    #     print (publication['post'], publication['photo'])
    paginator = Paginator(news_page_posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    content = {
        'title': title,
        'posts': posts,
    }
    return render(request, 'mainapp/news.html', content)

def details(request, pk):
    post = Post.objects.get(pk=pk)
    photos = Photo.objects.filter(post_id=pk)
    title = 'РСПС - Новости'
    content = {
        'title': title,
        'post': post,
        'photos': photos,
    }
    return render(request, 'mainapp/news_detail.html', content)

def docs(request):
    title = 'РСПС - Документы'
    content = {
        'title': title
    }
    return render(request, 'mainapp/docs.html', content)

def regional_office(request):
    title = 'РСПС - Региональные отделения'
    content = {
        'title': title
    }
    return render(request, 'mainapp/regional_office.html', content)

def regional_office_detail(request):
    title = 'РСПС - Региональное отделение'
    content = {
        'title': title
    }
    return render(request, 'mainapp/regional_office_detail.html', content)

def reestr(request):
    title = 'РСПС - Реестр членов'
    content = {
        'title': title
    }
    return render(request, 'mainapp/reestr.html', content)

def conf(request):
    title = 'РСПС - Конференции'
    content = {
        'title': title
    }
    return render(request, 'mainapp/conf.html', content)
