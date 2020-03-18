from django.contrib import admin

from rules.contrib.admin import ObjectPermissionsModelAdmin, ObjectPermissionsTabularInline

from report.models import Person

from .models import (
    Post,
    Task,
    Report,
    ReportAttachment,
)


@admin.register(Task)
class TaskAdmin(ObjectPermissionsModelAdmin):
    list_display = ('description', 'begin_date', 'end_date', 'deadline')
    list_display_links = ('description',)
    list_filter = ('description', 'deadline')
    search_fields = ('description',)
    ordering = ('-deadline',)


@admin.register(Post)
class PostAdmin(ObjectPermissionsModelAdmin):
    list_display = ('description', 'members_display')
    list_display_links = ('description',)
    ordering = ('code',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'members':
            kwargs['queryset'] = Person.objects.filter(user__is_staff=True).order_by('idnum')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def members_display(self, post):
        return '、'.join(person.name for person in post.members.all())
    members_display.short_description = '成员'


class ReportAttachmentInline(ObjectPermissionsTabularInline):
    model = ReportAttachment
    extra = 0


@admin.register(Report)
class ReportAdmin(ObjectPermissionsModelAdmin):
    list_display = ('task', 'post', 'add_time')
    list_display_links = ('task',)
    list_filter = ('task', 'post', 'add_time')
    search_fields = ('post__code', 'post__description', 'task__code', 'task__description', 'content')
    ordering = ('-add_time',)
    inlines = (ReportAttachmentInline,)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'post':
                kwargs['queryset'] = request.user.person.post_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        css = {
            'all': ('css/hide_admin_original.css',),
        }
