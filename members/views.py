from django.shortcuts import render
from mainapp.models import Member
from .models import Membership, MemberRegistration
from .forms import MemberForm, EditMemberForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.core import serializers
# from django.utils.html import format_html

# Create your views here.

class StatusedMember:
    def __init__(self, member_pk):
        self.member = Member.objects.get(pk=member_pk)
        self.pk = member_pk
        self.status = self.status_get_or_create()
        self.fio = self.member.fio
        self.job = self.member.job
        self.jobplace = self.member.jobplace
        self.email = self.member.email
        self.tel = self.member.tel

    def status_get_or_create(self):
        try:
            self.membership = Membership.objects.get(member=self.member)
        except Membership.DoesNotExist:
            self.membership = Membership.objects.create(member=self.member)
        return self.membership.status

    def set_status(self, status):
        self.membership.status = status
        self.membership.save()

def member_list(request):
    title = 'Список членов РСПС'
    member_list = Member.objects.all()
    members = []

    for member in member_list:
        statused_member = StatusedMember(member.pk)
        members.append(statused_member)

    if request.method == "POST":
        print('REQUEST POST', request.POST)
        add_new_member_form = MemberForm(request.POST)
        if add_new_member_form.is_valid():
            new_member = add_new_member_form.save(commit=False)
            new_member.user = request.user
            filtered_by_name = Member.objects.filter(fio=request.POST['fio'])
            if len(filtered_by_name) > 0:
                not_unique_message = {
                        'not_unique': 'member fio not unique',
                        'member_fio': request.POST['fio'],
                        'member_id': filtered_by_name[0].pk
                        }
                print(not_unique_message)
                return JsonResponse(not_unique_message)
            else:
                new_member.save()
                statused_member = StatusedMember(new_member.pk)
                statused_member.status_get_or_create()
                statused_member.set_status('Заявлен')
            # return HttpResponseRedirect(reverse('members:member_list'))
            success_message = {'new_member_saved': new_member.pk}
            return JsonResponse(success_message)
        else:
            errors = add_new_member_form.errors
            print(add_new_member_form.errors.as_json())
            return JsonResponse(errors)

    else:
        add_new_member_form = MemberForm()

    #pagination
    paginator = Paginator(members, 10)
    page = request.GET.get('page')
    paginated_members = paginator.get_page(page)

    content = {
        'title': title,
        'members': paginated_members,
        'add_new_member_form': add_new_member_form,
        'success': 'success',
        #TODO: add edit form for every member
    }

    return render(request, 'members/lk_member_list.html', content)

def get_member_form(request):
    if request.method == 'POST':
        print('REQUEST POST', request.POST)
        member_pk = request.POST.get('member_pk')
        edit_member = Member.objects.get(pk=member_pk)
        edit_member_form = EditMemberForm(instance=edit_member)
        membership = Membership.objects.get(member=edit_member)
        print('STATUS:', membership.status)
        if 'update_form_data' in request.POST:
            if 'register_new_member' in request.POST:
                membership.status = 'Заявлен'
                membership.save()
            if request.POST.get('event_register', '') == 'on':
                registration = MemberRegistration.objects.create(
                    member=edit_member,
                    name='Зарегистрирован на Съезд 2019',
                    register=True,
                    )
                registration.save()
            form_updating = EditMemberForm(request.POST or None, instance=edit_member)
            if form_updating.is_valid():
                form_updating.save()
                success_message = {
                    'success': True,
                    'id': edit_member.pk,
                    'message': '<span class="text-info"> \
                                <i class="fa fa-check mr-2"></i>\
                                Успешно сохранено</span>',
                }
                return JsonResponse(success_message)
            else:
                errors = form_updating.errors
                errors['message'] = '<span class="text-danger">\
                                     <i class="fa fa-times mr-2"></i>\
                                     Ошибка сохранения</span>',
                return JsonResponse(errors)
        # print(member_pk)

        registrations = MemberRegistration.objects.filter(member=edit_member)

        context = {
            'member': edit_member,
            'membership': membership,
            'registrations': registrations,
            'member_edit_form': edit_member_form,
        }
        return render(request, 'members/includes/member_edit_form.html', context)