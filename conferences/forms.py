from django import forms

from mainapp.models import Conference

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