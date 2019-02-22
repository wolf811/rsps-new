from django.shortcuts import render

# Create your views here.
def member_list(request):
    return render(request, 'members/lk_member_list.html')