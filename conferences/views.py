from django.shortcuts import render
from django.http import HttpResponse
from mainapp.models import Conference
from .models import ConferenceTheme
from mainapp.models import Member
from .forms import ConferenceForm, ConferenceEditForm, SubjectForm
from members.forms import MemberForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
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
    current_user_members = Member.objects.filter(user=request.user)

    content = {
        'add_new_conference_form': new_conference_form,
        'conferences': paginated_conferences,
        'members': current_user_members
    }
    return render(request, 'conferences/conferences_list.html', content)

@login_required
def edit_conference(request):
    SubjectFormSet = modelformset_factory(ConferenceTheme, form=SubjectForm, can_delete=True)
    try:
        edit_conference = Conference.objects.get(pk=request.POST.get('conference_id'))
    except Exception as e:
        print ('ERROR', e)
        return JsonResponse({'server_error': e.__dict__})
    questions = ConferenceTheme.objects.filter(conference=edit_conference)
    if request.method == 'POST':
        if request.POST.get('saving_conference'):
            conference_form = ConferenceEditForm(request.POST, instance=edit_conference)
            if conference_form.is_valid():
                conference_form.save()
            formset = SubjectFormSet(request.POST)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for subj in instances:
                    subj.conference = edit_conference
                    subj.save()
                formset.save()
                success_message = {
                    'message': '<b class="text-success">Успешно сохранено</b>',
                    'conference_id': request.POST.get('conference_id')}
                return JsonResponse(success_message)
            else:
                errors = {'formset_errors': formset.errors, 'message': 'Ошибка сохранения'}
                print('ERRORS', errors)
                return JsonResponse(errors)
        edit_conference_form = ConferenceEditForm(instance=edit_conference)
        formset = SubjectFormSet(queryset=questions)

        content = {
            'conference': edit_conference,
            'question_formset': formset,
            'edit_conference_form': edit_conference_form,
        }
        return render(request, 'conferences/includes/conference_edit.html', content)

def update_members(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    if request.method == 'POST':
        if request.POST.get('register_existitng_members'):
            # check if user wants to uncheck registrations
            # if len(request.POST.get('register_existing_members')) < conference.members.count():
            # add new registrations
            request_members = []
            for element in request.POST:
                if element.startswith('member_'):
                    member_pk = element.split('_')[1]
                    member = get_object_or_404(Member, pk=member_pk)
                    request_members.append(member)
                    if member not in conference.members.all():
                        conference.members.add(member)
            for member in conference.members.all():
                if member not in request_members:
                    conference.members.remove(member)
            return JsonResponse({'status': 'ok',
                                 'conference_id': conference.pk})
                    # pdb.set_trace()
        if request.POST.get('register_new_member_adding_to_conference'):
            print(request.POST)
            form = MemberForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                conference.members.add(instance)
                return JsonResponse({'new_member_saved_and_registered_to_conference': 'True'})
            else:
                errors = form.errors
                # pdb.set_trace()
                return JsonResponse({'member_save_errors': True, 'errors': errors})

        return JsonResponse({'status': 'ok'})

def get_list_of_members(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    list_of_registrations = conference.members.all()
    if request.POST.get('get_checkboxes'):
        return JsonResponse({'checkboxes': ['member_{}'.format(obj.pk) for obj in list_of_registrations]})
    content = {
        'conference': conference,
        'list_of_registrations': list_of_registrations
    }
    return render(request, 'conferences/includes/list_of_registrations.html', content)

def unregister_members(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    member = request.POST.get('unregister_member')
    conference.members.remove(member)
    # pdb.set_trace()
    return JsonResponse({'status': 'ok',
                         'deleted_member_registration': 'True',
                         'conference_id': conference.pk})

def delete_conference(request):
    return 'delete conference'
