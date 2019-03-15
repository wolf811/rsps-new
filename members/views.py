from django.shortcuts import render
from mainapp.models import Member
from .models import Membership, MemberRegistration
from .forms import MemberForm, EditMemberForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.core import serializers
import re
from django.db.models import Q
from django import forms

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
        self.registrations = self.get_registrations()

    def status_get_or_create(self):
        try:
            self.membership = Membership.objects.get(member=self.member)
        except Membership.DoesNotExist:
            self.membership = Membership.objects.create(member=self.member)
        return self.membership.status

    def set_status(self, status):
        self.membership.status = status
        self.membership.save()

    def get_registrations(self):
        return MemberRegistration.objects.filter(member=self.member)

def member_list(request):
    title = 'Список членов РСПС'
    member_list = Member.objects.filter(user=request.user) #TODO: fix to filter by request user
    members = []

    for member in member_list:
        statused_member = StatusedMember(member.pk)
        members.append(statused_member)

    # print('CITIES', cities)
    USER_CITIES = [('All', 'Все')]
    USER_CITIES += [(member.member.city, member.member.city) for member in members]
    USER_CITIES = tuple(USER_CITIES)

    from .models import STATUS_CHOICES
    statuses = list(STATUS_CHOICES)
    default_status = [('All', 'Все')]
    STATUS_CHOICES = tuple(default_status+statuses)

    class SearchMemberForm(forms.Form):
        fio_city_job = forms.CharField(required=False, max_length=100)
        city = forms.ChoiceField(choices=USER_CITIES, required=False, )
        status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    search_member_form = SearchMemberForm()

    if request.method == "POST":
        print('REQUEST POST', request.POST)
        add_new_member_form = MemberForm(request.POST)
        #handle member search
        if 'search_member' in request.POST:
            form = SearchMemberForm(request.POST)
            if form.is_valid():
                fio_city_job_query = Q()
                if request.POST['fio_city_job'] != '':
                    fio_city_job_query = Q(fio__icontains=request.POST['fio_city_job'])
                    fio_city_job_query |= Q(jobplace__icontains=request.POST['fio_city_job'])
                    fio_city_job_query |= Q(job__icontains=request.POST['fio_city_job'])
                if request.POST['city'] != 'All':
                    fio_city_job_query &= Q(city=request.POST['city'])
                if request.POST['status']!= 'All':
                    filtered_statuses = Membership.objects.filter(status=request.POST['status'])
                    filtered_member_pks = [status.member.pk for status in filtered_statuses]
                    fio_city_job_query &= Q(id__in=filtered_member_pks)
                fio_city_job_query &= Q(user=request.user)
                filtered_members = Member.objects.filter(fio_city_job_query)
                filtered_statused_members = [StatusedMember(member.pk) for member in filtered_members]
                # print('QUERY', fio_city_job_query)
                content = {
                    'title': title,
                    'members': filtered_statused_members,
                    'add_new_member_form': add_new_member_form,
                    'search_member_form': form,
                    'search_result_count': len(filtered_statused_members)
                }

                return render(request, 'members/lk_member_list.html', content)

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
        'search_member_form': search_member_form,
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
        if 'update_form_data' in request.POST:
            if 'register_new_member' in request.POST:
                membership.status = 'Заявлен'
                membership.save()
            annual_registrations = MemberRegistration.objects.filter(member=edit_member,
                                                                        name='Зарегистрирован на Съезд РСПС 2019',
                                                                        register=True)
            if request.POST.get('annual_event_register') == 'on':
                if annual_registrations.count() == 0:
                    MemberRegistration.objects.create(member=edit_member,
                                                      name='Зарегистрирован на Съезд РСПС 2019')
            #check if user unchek a registration

            form_updating = EditMemberForm(request.POST or None, instance=edit_member)
            if 'unregister_event' in request.POST:
                MemberRegistration.objects.get(pk=request.POST['unregister_event']).delete()
            if 'registered_event' in request.POST:
                if MemberRegistration.objects.filter(pk=request.POST['registered_event']).count() == 0:
                    MemberRegistration.objects.create(member=edit_member, name='Зарегистрирован на Съезд РСПС 2019')
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

        context = {
            'member': edit_member,
            'membership': membership,
            'member_edit_form': edit_member_form,
        }

        registrations = MemberRegistration.objects.filter(member=edit_member)

        if registrations.count() > 0:
            context['registrations'] = registrations

        return render(request, 'members/includes/member_edit_form.html', context)