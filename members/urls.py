from django.urls import path

import members.views as members

app_name = 'members'

urlpatterns = [
    path('list/', members.member_list, name='member_list'),
    path('edit/', members.get_member_form),
    path('delete/', members.delete_member, name='member_delete'),
    # path('new/', vacancies.add_new_vacancy, name='member_create'),
    # path('update/<slug:pk>', vacancies.vacancy_update, name='member_update'),
    # path('details/<slug:pk>', vacancies.member_details, name='member_details'),
]