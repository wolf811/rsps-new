from django import forms

from mainapp.models import Member


class MemberForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'
    class Meta:
        model = Member
        fields = ('fio', 'job', 'jobplace', 'tel', 'email', 'city',
                  'subscription')


class EditMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('fio', 'job', 'jobplace', 'tel', 'email', 'city',
                  'short_description', 'subscription')
        widgets= {
            'short_description': forms.Textarea(attrs={'rows': 3}),
            }

class SearchMemberForm(forms.Form):
    fio_city_job = forms.CharField(max_length=100)
