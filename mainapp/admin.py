from django.contrib import admin
from mainapp.models import Conference
from mainapp.models import Member, Post, Photo
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.

def get_picture_preview(obj):
    if obj.pk:  # if object has already been saved and has a primary key, show picture preview
        return format_html("""<a href="{src}" target="_blank">
        <img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" />
        </a>""".format(
            src=obj.image.url,
            title=obj.title,
        ))
    return "(После загрузки фотографии здесь будет ее миниатюра)"

class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 0
    fields = ['image', get_picture_preview]
    readonly_fields = [get_picture_preview]

    def get_edit_link(self, obj=None):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (
                obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return format_html("""<a href="{url}">{text}</a>""".format(
                url=url,
                text="Редактировать %s отдельно" % obj._meta.verbose_name,
            ))
        return "(Загрузите фотографию и нажмите \"Сохранить и продолжить редактирование\")"
    get_edit_link.short_description = "Изменить"
    get_edit_link.allow_tags = True

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    view_on_site = True
    fields = ('title', 'text', 'published_date')
    list_display = ['title', 'published_date']
    inlines = [PhotoInline]

    def view_on_site(self, obj):
        url = reverse('details', kwargs={'pk': pk})
        return url


admin.site.register(Conference)
admin.site.register(Member)

