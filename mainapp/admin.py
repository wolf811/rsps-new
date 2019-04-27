from django.contrib import admin
from mainapp.models import Conference
from mainapp.models import Member, Post, Photo
from members.models import Membership, MemberRegistration
from conferences.models import ConferenceTheme
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.

def get_picture_preview(obj):
    if obj.pk:  # if object has already been saved and has a primary key, show picture preview
        return format_html("""<a href="{src}" target="_blank">
        <img src="{src}" alt="title" style="max-width: 200px; max-height: 200px;" />
        </a>""".format(src=obj.image.url))
    return "(После загрузки фотографии здесь будет ее миниатюра)"

class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
    fields = ['status']

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

class ConferenceThemeInline(admin.StackedInline):
    model = ConferenceTheme
    extra = 0
    fields = ['subject']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    view_on_site = True
    fields = ('title', 'short_description', 'text', 'published_date')
    list_display = ['title', 'published_date', 'user']
    inlines = [PhotoInline]

    def view_on_site(self, obj):
        url = reverse('details', kwargs={'pk': obj.pk})
        return url

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if getattr(instance, 'user', None) is None:
            instance.user = request.user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    view_on_site = False
    fields = ['fio', 'job', 'jobplace', 'tel', 'email', 'user']
    inlines = [MembershipInline]

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    view_on_site = False
    exclude = ()
    inlines = [ConferenceThemeInline]

# admin.site.register(Conference)
# admin.site.register(Photo)

def generate_sha(file):
    sha = hashlib.sha1()
    file.seek(0)
    while True:
        buf = file.read(104857600)
        if not buf:
            break
        sha.update(buf)
    sha1 = sha.hexdigest()
    file.seek(0)

    return sha1

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        sha = generate_sha(obj.image)
        obj.file_sha1 = sha
        match_qs = ReportPost.objects.filter(file_sha1=sha)
        if match_qs.count() > 0:
            obj.image = match_qs[0].file
        obj.save()

admin.site.register(MemberRegistration)
admin.site.register(Membership)