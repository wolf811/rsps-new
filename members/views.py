from django.shortcuts import render
from mainapp.models import Member
from .models import Membership
from .forms import MemberForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

class StatusedMember:
    def __init__(self, member_pk):
        self.member = Member.objects.get(pk=member_pk)
        self.status = Membership.objects.create(member=self.member)
        self.fio = self.member.fio
        self.job = self.member.job
        self.jobplace = self.member.jobplace
        self.email = self.member.email
        self.tel = self.member.tel

def member_list(request):
    title = 'Список членов РСПС'
    member_list = Member.objects.all()
    members = []

    for member in member_list:
        statused_member = StatusedMember(member.pk)
        members.append(statused_member)

    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            new_member = form.save(commit=False)
            new_member.user = request.user
            new_member.save()
            return HttpResponseRedirect(reverse('members:member_list'))
    else:
        form = MemberForm()

    print(members)

    content = {
        'title': title,
        'members': members,
        'form': form,
    }

    return render(request, 'members/lk_member_list.html', content)