from django.shortcuts import render
from django.http import HttpResponse
from mainapp.models import Conference, Photo
from .models import ConferenceTheme
from mainapp.models import Member, Post
from .forms import ConferenceForm, ConferenceEditForm, SubjectForm, FileUploadForm, PhotoForm
from django.core.files import File
from mainapp.forms import PostEditForm
from members.forms import MemberForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.utils import timezone
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
    SubjectFormSet = modelformset_factory(ConferenceTheme, form=SubjectForm,
        fields=('subject',), can_delete=True)
    try:
        edit_conference = Conference.objects.get(pk=request.POST.get('conference_id'))
    except Exception as e:
        print ('ERROR', e)
        return JsonResponse({'server_error': e.__dict__})
    questions = ConferenceTheme.objects.filter(conference=edit_conference)
    if request.method == 'POST':
        if request.POST.get('saving_conference'):
            conference_form = ConferenceEditForm(request.POST, instance=edit_conference)
            # import pdb; pdb.set_trace()
            if conference_form.is_valid():
                instance = conference_form.save()
                instance.save()
            else:
                return JsonResponse({'conference_form_errors': conference_form.errors})
            formset = SubjectFormSet(request.POST)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for subj in instances:
                    subj.conference = edit_conference
                    subj.save()
                formset.save()
                success_message = {
                    'message': """<span class="text-success">
                                    <i class="fa fa-check mr-2"></i>
                                    Успешно сохранено
                                </span>""",
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
    conference = get_object_or_404(Conference,
            pk=request.POST.get('remove_conference_with_id'))
    conference.delete()
    return JsonResponse({'removed_conference': conference.pk})

def get_publication_form(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    # return JsonResponse({'success': conference.pk})
    if not conference.publication:
        post_data = {
            'title': conference.title,
            'short_description': 'Состоялась региональная конференция "{}"'.format(conference.title),
            'text': """<p><b>Завершена региональная конференция</b></p>
            <p><strong>Вопросы повестки дня:</strong></p>
            {}
            <p><strong>Участники конференции:</strong></p>
            {}
            """.format(
                '<br>'.join([t.subject for t in ConferenceTheme.objects.filter(conference=conference)]),
                '<br>'.join([member.fio for member in conference.members.all()])
                ),
            # 'published_date': None,
            }
        form = PostEditForm(initial=post_data)
        # upload_form = FileUploadForm()
    else:
        form = PostEditForm(instance=conference.publication)
    # new_post.save()
    content = {
        'form': form,
        # 'upload_form': upload_form,
    }
    return render(request, 'mainapp/includes/post_edit_form.html', content)


def save_conference_publication(request, conference_id):
    # pdb.set_trace()
    conference = get_object_or_404(Conference, pk=conference_id)
    form_data = {
        'title': request.POST.get('title'),
        'short_description': request.POST.get('short_description'),
        'text': request.POST.get('updated_text')
    }
    form = PostEditForm(form_data, instance=conference.publication or None)
    # import pdb; pdb.set_trace()
    # pdb.set_trace()
    if form.is_valid():
        instance = form.save(commit=False)
        instance.published_date = timezone.now()
        instance.user = request.user
        instance.save()
        conference.publication = instance
        if len(request.FILES) > 0:
            # for f in request.FILES('images'):
            image_uploading_errors = []
            for f in request.FILES.getlist('images'):
                photo = Photo(image=File(f), post=instance)
                # pdb.set_trace()
                if photo.clean():
                    try:
                        photo.save()
                    except Exception as e:
                        print('ERROR:', e)
                        image_uploading_errors.append('{}:{}'.format(f.name, e))
                else:
                    return JsonResponse({'error': 'ERROR IMAGE SAVING'})

        conference.save()

        server_message = {
            'message': 'Публикация сохранена',
            'publication_id': '{}'.format(conference.publication.pk),
        }

        if len(request.FILES) !=0 and len(image_uploading_errors) > 0:
            # import pdb; pdb.set_trace()
            server_message['image_uploading_error'] = image_uploading_errors

        return JsonResponse(server_message)
    else:
        errors = form.errors
        return JsonResponse({'message': 'Публикация не сохранена'})

def edit_conference_publication(request, publication_id):
    publication = get_object_or_404(Post, pk=publication_id)
    print('PUBLICATION', publication)
    edit_publication_form = PostEditForm(instance=publication)
    photos = Photo.objects.filter(post__pk=publication.pk)
    # if edit_publication_form.is_valid():
    #     edit_publication_form.save()
    #     return JsonResponse({'message': 'Успешно сохранено'})
    # else:
    #     print(edit_publication_form.errors.as_data())
    #     return JsonResponse({'message': 'Ошибка сохранения', 'errors': edit_publication_form.errors})
    # import pdb; pdb.set_trace()
    content = {
        'form': edit_publication_form,
        'photos': photos,
    }
    return render(request, 'mainapp/includes/post_edit_form.html', content)

def delete_conference_publication(request, publication_id):
    publication = get_object_or_404(Post, pk=publication_id)
    print('DELETING', publication)
    publication.delete()
    return JsonResponse({'message': 'Удалено'})

def update_conference_row(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    print('UPDATING_ROW', conference)
    content = {
        'conference': conference
    }
    return render(request, 'conferences/includes/conference_row.html', content)

def delete_publication_photo(request, photo_id):
    # pdb.set_trace()
    photo = get_object_or_404(Photo, pk=photo_id)
    photo.delete()
    return JsonResponse({'photo_deleted': photo_id})

def get_uploaded_files(request, publication_id):
    publication = get_object_or_404(Post, pk=publication_id)
    photos = Photo.objects.filter(post=publication)
    return render(request, 'mainapp/includes/uploaded_files.html', {'photos': photos})