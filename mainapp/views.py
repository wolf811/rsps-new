from django.shortcuts import render
from mainapp.models import Conference
from mainapp.models import Member
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
	content = {
		'title': title
	}
	return render(request, 'mainapp/news.html', content)

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

def conf(request):
	title = 'РСПС - Конференции'
	content = {
		'title': title
	}
	return render(request, 'mainapp/conf.html', content)
