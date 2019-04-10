from django import forms
from .models import Post
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget


class PostEditForm(forms.ModelForm):
    # title = forms.CharField()
    # short_description = forms.CharField()
    text = forms.CharField(
        label="Текст публикации",
        widget=CKEditorWidget(config_name='minified_config')
        )

    class Meta:
        model = Post
        exclude = ('user', 'published_date',)

    # widgets = {
    #         'text': RichTextUploadingField(config_name='minified_config'),
    #     }


