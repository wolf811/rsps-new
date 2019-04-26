from django import forms

from mainapp.models import Conference, Photo
from conferences.models import ConferenceTheme

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference

        fields = ('title', 'date', 'place')
        widgets = {
            'date': forms.TextInput({
                'placeholder': "дд.мм.гггг",
                'aria-label': "дд.мм.гггг",
                'aria-describedby': "",
                }),
        }

class ConferenceEditForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ('title', 'date', 'place', 'completed')
        widgets = {
            'date': forms.TextInput({
                'placeholder': "дд.мм.гггг",
                'aria-label': "дд.мм.гггг",
                'aria-describedby': "",
                }),
        }

class SubjectForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput({
                'type': "text",
                'class': "form-control form-control-sm",
                'placeholder': 'Введите вопрос повестки дня',
                }), label='')

class FileUploadForm(forms.Form):
    images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs=
        {'multiple': True}))

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('post',)