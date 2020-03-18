from django.contrib import admin

from .models import Notice, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    fields = ('file', 'weight', 'add_time', 'update_time')
    readonly_fields = ('add_time', 'update_time')
    extra = 0


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    readonly_fields = ('add_time', 'update_time')
    list_display = ('title', 'post_time', 'source', 'published', 'to_ack', 'marked')
    list_filter = ('published', 'to_ack', 'marked', 'source')
    ordering = ('-post_time',)
    search_fields = ('title', 'source')
    inlines = (AttachmentInline,)

    class Media:
        css = {
            'all': ('css/hide_admin_original.css',),
        }
