from django.shortcuts import render
from django.http import HttpResponse
from mainapp.models import Conference
from .models import ConferenceTheme
from .forms import ConferenceForm, ConferenceEditForm, SubjectForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import modelformset_factory
import pdb

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

@login_required
def edit_conference(request):
    # SubjectFormSet = modelformset_factory(ConferenceTheme, form=SubjectForm)
    SubjectFormSet = modelformset_factory(ConferenceTheme, form=SubjectForm, can_delete=True)
    edit_conference = Conference.objects.get(pk=request.POST.get('conference_id'))
    questions = ConferenceTheme.objects.filter(conference=edit_conference)
    if request.method == 'POST':
        print('REQUEST POST', request.POST)
        if request.POST.get('saving_conference'):
            formset = SubjectFormSet(request.POST)
            # pdb.set_trace()
            if formset.is_valid():
                formset.save()
                success_message = {
                    'message': '<b class="text-success">recieved</b>',
                    'conference_id': request.POST.get('conference_id')}
                return JsonResponse(success_message)
            else:
                errors = {'errors': formset.errors}
                print('ERRORS', errors)
                return JsonResponse(errors)
        edit_conference_form = ConferenceEditForm(instance=edit_conference)
        formset = SubjectFormSet(queryset=questions)
        content = {
            'conference': edit_conference,
            # 'questions': questions,
            'question_formset': formset,
            'edit_conference_form': edit_conference_form
        }
        return render(request, 'conferences/includes/conference_edit.html', content)


def delete_conference(request):
    return 'delete conference'
