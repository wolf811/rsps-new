from django.shortcuts import render
from django.http import HttpResponse
from mainapp.models import Conference
from .models import ConferenceTheme
from .forms import ConferenceForm, ConferenceEditForm, SubjectForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory

# Create your views here.
# path('list/', conferences.conference_list, name='member_list'),
# path('edit/', conferences.get_conference),
# path('delete/', conferences.delete_conference, name='member_delete'),

@login_required
def conference_list(request):
    conferences = Conference.objects.filter(user=request.user).order_by('-date')
    new_conference_form = ConferenceForm()
    if request.method == 'POST':
        new_conference = ConferenceForm(request.POST)
        request_user = request.POST.get('username')
        user = User.objects.get(username=request_user)
        if new_conference.is_valid():
            new_conf = new_conference.save(commit=False)
            new_conf.user = user
            new_conf.save()
            success_message = {
                'success': 'ok',
                'message:': 'Конференция сохранена',
            }
            return JsonResponse(success_message)
        else:
            errors = new_conference.errors
            return JsonResponse(errors)

    paginator = Paginator(conferences, 10)
    page = request.GET.get('page')
    paginated_conferences = paginator.get_page(page)

    content = {
        'add_new_conference_form': new_conference_form,
        'conferences': paginated_conferences,
    }
    return render(request, 'conferences/conferences_list.html', content)


def edit_conference(request):
    edit_conference = Conference.objects.get(id=request.POST.get('conference_id'))
    edit_conference_form = ConferenceEditForm(instance=edit_conference)
    questions = ConferenceTheme.objects.filter(conference=edit_conference)
    SubjectFormSet = formset_factory(SubjectForm, extra=1)
    formset = SubjectFormSet(initial=[
        {'subject': question.subject} for question in questions])
    print('FORMSET', formset)
    content = {
        'conference': edit_conference,
        # 'questions': questions,
        'question_formset': formset,
        'edit_conference_form': edit_conference_form
    }
    return render(request, 'conferences/includes/conference_edit.html', content)


def delete_conference(request):
    return 'delete conference'
