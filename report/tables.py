import itertools

from django.urls import reverse
from django.conf import settings
from django.utils.html import format_html

import django_tables2 as tables
from django_tables2.utils import A

from .models import Record, Entry, Building


class RecordTable(tables.Table):
    date = tables.DateColumn(settings.MONTH_DAY_FORMAT)
    symptom = tables.Column('健康状况', accessor='pk')

    def render_symptom(self, value, record):
        symptoms = []
        for symptom in ['fever', 'cough', 'wornout']:
            field_name = 'has_' + symptom
            if getattr(record, field_name):
                symptoms.append(getattr(Record, field_name).field.verbose_name)
        if symptoms:
            text = '、'.join(symptoms)
            color = 'warning'
        else:
            text = '健康'
            color = 'success'
        return format_html('<span class="text-{}">{}</span>', color, text)

    class Meta:
        model = Record
        fields = ('date', 'symptom', 'temperature')
        order_by = ('-date',)
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-sm table-striped'}
        empty_text = '您还没有健康打卡记录。'


class EntryTable(tables.Table):
    date = tables.DateColumn(settings.MONTH_DAY_FORMAT, verbose_name='进楼日期')
    add_time = tables.DateTimeColumn(settings.SHORT_DATETIME_FORMAT, verbose_name='申请时间')
    status = tables.Column('状态', accessor='pk')
    action = tables.Column('操作', accessor='pk', orderable=False)

    def render_status(self, value, record):
        status = ('尚未审批', 'secondary')
        if record.approve1_decision is not None:
            status = ('部门审批通过', 'info') if record.approve1_decision else ('部门审批不通过', 'danger')
        if record.approve2_decision is not None:
            status = ('干事审批通过', 'info') if record.approve2_decision else ('干事审批不通过', 'danger')
        if record.approve3_decision is not None:
            status = ('审批通过', 'success') if record.approve3_decision else ('主管审批不通过', 'danger')
        content, color = status
        return format_html('<span class="text-{}">{}</span>', color, content)

    def render_action(self, value):
        return format_html(
            '<a href="{}">修改</a> <a href="{}" class="text-danger">删除</a>',
            reverse('report:entry_detail', args=(value,)),
            reverse('report:entry_delete', args=(value,)),
        )

    class Meta:
        model = Entry
        fields = ('date', 'building', 'room', 'purpose', 'add_time')
        order_by = ('-date',)
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-sm table-striped'}
        empty_text = '您还没有提交过进楼申请。'


class BuildingTable(tables.Table):
    name = tables.LinkColumn('report:building_detail', args=[A('uuid')])
    url = tables.Column('审批通过清单地址', accessor='pk', orderable=False)
    weight = tables.Column(visible=False)

    def render_url(self, record):
        return 'https://r.cs.tsinghua.edu.cn/building/{}/'.format(record.uuid)

    class Meta:
        model = Building
        fields = ('name', 'url', 'weight')
        order_by = ('-weight', 'name')
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-sm table-striped'}
        empty_text = '尚未添加楼宇。'


class BuildingEntryTable(tables.Table):
    nr = tables.Column('序号', empty_values=(), orderable=False)
    category = tables.Column('类型', accessor='person__idnum')
    building__name = tables.Column('楼宇')
    date = tables.DateColumn(settings.MONTH_DAY_FORMAT, verbose_name='进楼日期')
    is_valid = tables.Column('符合要求', empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_counter = itertools.count(1)

    def value_nr(self):
        return next(self.row_counter)

    def render_nr(self):
        return str(next(self.row_counter))

    def render_person__phone(self, value):
        return value.as_national

    def render_category(self, value):
        code = value[4:6]
        if code[0] in '69':
            if code == '66':
                category = '博士后'
            else:
                category = '教工'
        elif code[0] in '0123':
            category = '学生'
        else:
            category = '其他'
        return category

    def value_date(self, value):
        return value

    def value_is_valid(self):
        return '是'

    def render_is_valid(self):
        return '是'

    class Meta:
        model = Entry
        fields = (
            'nr',
            'person__name',
            'person__affiliation',
            'person__phone',
            'person__idnum',
            'category',
            'building__name',
            'date',
            'room',
            'purpose',
            'is_valid',
        )
        order_by = ('person__idnum',)
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-sm table-striped'}
        empty_text = '今日没有审批通过的进楼申请。'
