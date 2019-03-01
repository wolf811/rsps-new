from django.shortcuts import render
from mainapp.models import Member
from .models import Membership
from .forms import MemberForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
import json


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
        status = [x for x in Membership.objects.filter(member=self.member)]
        if len(status) == 0:
            membership = Membership.objects.create(member=self.member)
            status.append(membership)
        else:
            for m in status:
                if status.index(m) > 0:
                    status.remove(m)
                    m.delete()
        return status[0]

    def set_status(self, status):
        current_status = self.status_get_or_create()
        current_status.status = status

def member_list(request):
    title = 'Список членов РСПС'
    member_list = Member.objects.all()
    members = []

    for member in member_list:
        statused_member = StatusedMember(member.pk)
        members.append(statused_member)

    if request.method == "POST":
        print(request.POST)
        add_new_member_form = MemberForm(request.POST)
        if add_new_member_form.is_valid():
            new_member = add_new_member_form.save(commit=False)
            new_member.user = request.user
            new_member.save()
            return HttpResponseRedirect(reverse('members:member_list'))
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