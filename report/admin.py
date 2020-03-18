import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from rules.contrib.admin import ObjectPermissionsModelAdmin, ObjectPermissionsTabularInline

from . import utils
from .models import (
    Organization,
    Person,
    Record,
    Building,
    Entry,
)


@admin.register(Organization)
class OrganizationAdmin(ObjectPermissionsModelAdmin):
    list_display = ('name', 'code', 'parent')
    ordering = ('code',)
    search_fields = ('code', 'name')


class RecordInline(ObjectPermissionsTabularInline):
    model = Record
    fields = ('date', 'is_healthy', 'temperature', 'add_time', 'ip_with_city')
    readonly_fields = fields
    ordering = ('-add_time',)
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def ip_with_city(self, obj):
        city = utils.city_of_ip(obj.ip)
        if city:
            return obj.ip + ' (' + city + ')'
        return obj.ip
    ip_with_city.short_description = Record.ip.field.verbose_name


class RegisteredFilter(admin.SimpleListFilter):
    title = '已注册'
    parameter_name = 'registered'

    def lookups(self, request, model_admin):
        return (
            ('1', '是'),
            ('0', '否'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == '1':
            return queryset.filter(user__isnull=False)
        elif value == '0':
            return queryset.filter(user__isnull=True)
        else:
            return queryset


@admin.register(Person)
class PersonAdmin(ObjectPermissionsModelAdmin):
    list_display = ('idnum', 'name', 'department', 'category', 'phone', 'registered', 'no_record_days')
    list_display_links = ('idnum', 'name')
    list_filter = (RegisteredFilter, 'category', 'affiliation')
    ordering = ('idnum',)
    search_fields = ('idnum', 'name', 'affiliation__name', 'phone')
    autocomplete_fields = ('affiliation',)
    inlines = (RecordInline,)

    def no_record_days(self, obj):
        recent_time = obj.recent_record_time()
        if recent_time:
            return (timezone.now().date() - recent_time.date()).days
        else:
            return '从未'
    no_record_days.short_description = '未打卡天数'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            person = getattr(request.user, 'person', None)
            if person:
                queryset = queryset.filter(affiliation__in=person.can_contact.all())
        return queryset

    class Media:
        css = {
            'all': ('css/hide_admin_original.css',),
        }


@admin.register(Building)
class BuildingAdmin(ObjectPermissionsModelAdmin):
    ordering = ('-weight', 'name')


class SimpleDateFilter(admin.DateFieldListFilter):

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        today = timezone.localdate()
        one_day = datetime.timedelta(days=1)
        self.links = (
            ('任意日期', {}),
            ('前天（{}）'.format((today - one_day * 2).strftime('%-m月%-d日')), {
                self.lookup_kwarg_since: str(today - one_day * 2),
                self.lookup_kwarg_until: str(today - one_day),
            }),
            ('昨天（{}）'.format((today - one_day).strftime('%-m月%-d日')), {
                self.lookup_kwarg_since: str(today - one_day),
                self.lookup_kwarg_until: str(today),
            }),
            ('今天（{}）'.format(today.strftime('%-m月%-d日')), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + one_day),
            }),
            ('明天（{}）'.format((today + one_day).strftime('%-m月%-d日')), {
                self.lookup_kwarg_since: str(today + one_day),
                self.lookup_kwarg_until: str(today + one_day * 2),
            }),
            ('后天（{}）'.format((today + one_day * 2).strftime('%-m月%-d日')), {
                self.lookup_kwarg_since: str(today + one_day * 2),
                self.lookup_kwarg_until: str(today + one_day * 3),
            }),
            ('大后天（{}）'.format((today + one_day * 3).strftime('%-m月%-d日')), {
                self.lookup_kwarg_since: str(today + one_day * 3),
                self.lookup_kwarg_until: str(today + one_day * 4),
            }),
        )


@admin.register(Entry)
class EntryAdmin(ObjectPermissionsModelAdmin):
    list_display = (
        'person', 'date', 'building', 'room', 'purpose', 'add_time',
        'approve1_decision', 'approve2_decision', 'approve3_decision',
    )
    list_filter = (
        ('date', SimpleDateFilter),
        'approve1_decision', 'approve2_decision', 'approve3_decision',
    )
    ordering = ('-date', 'add_time')
    autocomplete_fields = ('person',)
    actions = ('approve', 'decline')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            person = getattr(request.user, 'person', None)
            if person:
                queryset = queryset.filter(
                    person__affiliation__in=person.can_approve1.union(
                        person.can_approve2.all(),
                        person.can_approve3.all(),
                    ).values('id')
                )
        return queryset

    def approve(self, request, queryset, decision=True):
        person = getattr(request.user, 'person', None)
        time = timezone.now()
        for entry in queryset.all():
            if person.can_approve1.filter(id=entry.person.affiliation.id):
                if entry.approve1_decision != decision:
                    entry.approve1_decision = decision
                    entry.approve1_person = person
                    entry.approve1_time = time
            if person.can_approve2.filter(id=entry.person.affiliation.id):
                if entry.approve2_decision != decision:
                    entry.approve2_decision = decision
                    entry.approve2_person = person
                    entry.approve2_time = time
            if person.can_approve3.filter(id=entry.person.affiliation.id):
                if entry.approve3_decision != decision:
                    entry.approve3_decision = decision
                    entry.approve3_person = person
                    entry.approve3_time = time
            entry.save()
    approve.short_description = '审核通过'

    def decline(self, request, queryset):
        self.approve(request, queryset, decision=False)
    decline.short_description = '审核不通过'
