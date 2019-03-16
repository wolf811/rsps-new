from django.shortcuts import render
from django.http import HttpResponse
from mainapp.models import Conference
from .forms import ConferenceForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

# Create your views here.
# path('list/', conferences.conference_list, name='member_list'),
# path('edit/', conferences.get_conference),
# path('delete/', conferences.delete_conference, name='member_delete'),


def conference_list(request):
    conferences = Conference.objects.all()
    new_conference_form = ConferenceForm()
    if request.method == 'POST':
        print(request.POST)
        new_conference = ConferenceForm(request.POST)
        if new_conference.is_valid():
            new_conference.save(commit=False)
            new_conference.user = request.user
            new_conference.save()
            success_message = {
                'success': 'ok',
                'message:': 'Конференция сохранена',
            }
            return JsonResponse(success_message)
        else:
            errors = new_conference.errors
            return JsonResponse(errors)
    
    content = {
        'add_new_conference_form': new_conference_form,
        'conferences': conferences,
    }
    return render(request, 'conferences/conferences_list.html', content)


def get_conference(request):
    return 'conference'


def delete_conference(request):
    return 'delete conference'
