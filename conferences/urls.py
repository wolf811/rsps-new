from django.urls import path

import conferences.views as conferences

app_name = 'conferences'

urlpatterns = [
    path('list/', conferences.conference_list, name='conference_list'),
    path('edit/', conferences.edit_conference, name='conference_edit'),
    path('<slug:conference_id>/update_members/', conferences.update_members, name='update_members'),
    path('<slug:conference_id>/get_list_of_members/', conferences.get_list_of_members, name='get_list_of_members'),
    path('<slug:conference_id>/unregister_members/', conferences.unregister_members, name='unregister_members'),
    path('delete/', conferences.delete_conference, name='conference_delete'),
    # path('new/', vacancies.add_new_vacancy, name='member_create'),
    # path('update/<slug:pk>', vacancies.vacancy_update, name='member_update'),
    # path('details/<slug:pk>', vacancies.member_details, name='member_details'),
]