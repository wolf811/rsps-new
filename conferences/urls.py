from django.urls import path

import conferences.views as conferences

app_name = 'conferences'

urlpatterns = [
    path('list/', conferences.conference_list, name='conference_list'),
    path('edit/', conferences.edit_conference, name='conference_edit'),
    path('<slug:conference_id>/update_members/', conferences.update_members, name='update_members'),
    path('<slug:conference_id>/get_list_of_members/', conferences.get_list_of_members, name='get_list_of_members'),
    path('<slug:conference_id>/unregister_members/', conferences.unregister_members, name='unregister_members'),
    path('get_publication_form/<slug:conference_id>/', conferences.get_publication_form, name='get_publication_form'),
    path('edit_conference_publication/<slug:publication_id>/', conferences.edit_conference_publication, name='edit_conference_publication'),
    path('delete_conference_publication/<slug:publication_id>/', conferences.delete_conference_publication, name='delete_conference_publication'),
    path('update_conference_row/<slug:conference_id>/', conferences.update_conference_row, name='update_conference_row'),
    path('delete/', conferences.delete_conference, name='conference_delete'),
    # path('new/', vacancies.add_new_vacancy, name='member_create'),
    # path('update/<slug:pk>', vacancies.vacancy_update, name='member_update'),
    # path('details/<slug:pk>', vacancies.member_details, name='member_details'),
]