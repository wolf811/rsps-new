from django.shortcuts import render

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

def account(request):
	title = 'РСПС - Личный кабинет'
	content = {
		'title': title
	}
	return render(request, 'mainapp/account.html', content)

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

def regionalOffice(request):
	title = 'РСПС - Региональные отделения'
	content = {
		'title': title
	}
	return render(request, 'mainapp/regional-office.html', content)

def approved(request):
	title = 'РСПС - Одобрено РСПС'
	content = {
		'title': title
	}
	return render(request, 'mainapp/approved.html', content)
