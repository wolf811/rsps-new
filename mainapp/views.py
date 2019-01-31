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
