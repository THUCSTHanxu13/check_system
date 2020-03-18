import uuid

from django.conf import settings
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Organization(models.Model):
    code = models.CharField('代码', max_length=10, unique=True, null=True, blank=True)
    name = models.CharField('名称', max_length=100)
    parent = models.ForeignKey('self', models.SET_NULL, null=True, blank=True, verbose_name='上级组织')

    class Meta:
        verbose_name = '组织'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Person(models.Model):
    idnum = models.CharField('工作证号', max_length=10, unique=True)
    name = models.CharField('姓名', max_length=100)
    affiliation = models.ForeignKey(Organization, models.CASCADE, verbose_name='单位')
    category = models.CharField('类别', max_length=10, blank=True)
    phone = PhoneNumberField('联系电话', help_text='最好填写手机号，如果是座机请加区号，如果是境外电话请加国际电话区号。')
    phone2 = PhoneNumberField('备用电话', blank=True, help_text='紧急联系人的电话，格式同上。')
    return_date = models.DateField('返京日期或计划返京日期', null=True, blank=True, help_text='若暂无返京计划，可留空。')
    remark = models.TextField('问题与意见', blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.SET_NULL, verbose_name='用户', null=True, blank=True)
    can_contact = models.ManyToManyField(Organization, related_name='contactors', blank=True, verbose_name='联系')
    can_approve1 = models.ManyToManyField(Organization, related_name='approvers1', blank=True, verbose_name='部门审核')
    can_approve2 = models.ManyToManyField(Organization, related_name='approvers2', blank=True, verbose_name='干事审核')
    can_approve3 = models.ManyToManyField(Organization, related_name='approvers3', blank=True, verbose_name='主管审核')
    is_welcomed = models.BooleanField('发送欢迎消息', default=False)

    def department(self):
        current = self.affiliation
        name = current.name
        while current.parent:
            current = current.parent
            name = current.name + '-' + name
        return name
    department.short_description = '部门'
    department.admin_order_field = 'affiliation'

    def registered(self):
        return bool(getattr(self, 'user', None))
    registered.short_description = '注册'
    registered.boolean = True
    registered.admin_order_field = 'user'

    def recent_record_time(self):
        recent_record = self.record_set.order_by('add_time').last()
        return recent_record.change_time if recent_record else None
    recent_record_time.short_description = '最近打卡时间'

    class Meta:
        verbose_name = '人员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Record(models.Model):
    person = models.ForeignKey(Person, models.CASCADE, verbose_name='人员')
    date = models.DateField('日期')
    temperature = models.DecimalField('体温', max_digits=3, decimal_places=1, null=True, blank=True)
    has_fever = models.BooleanField('发烧', default=False)
    has_cough = models.BooleanField('咳嗽', default=False)
    has_wornout = models.BooleanField('乏力', default=False)
    remark = models.TextField('其他状况说明', blank=True)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)
    change_time = models.DateTimeField('修改时间', auto_now=True)
    ip = models.GenericIPAddressField('IP')
    is_submitted = models.BooleanField('已提交', default=False)

    def is_healthy(self):
        if not self.is_submitted:
            return None
        return not (self.has_fever or self.has_cough or self.has_wornout)
    is_healthy.short_description = '健康状态'
    is_healthy.boolean = True

    class Meta:
        verbose_name = '健康打卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.person) + ' @' + str(self.date)


class Building(models.Model):
    uuid = models.UUIDField('内部编码', default=uuid.uuid4, unique=True)
    name = models.CharField('名称', max_length=100)
    weight = models.IntegerField('权重', default=0)

    class Meta:
        verbose_name = '楼宇'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Entry(models.Model):
    person = models.ForeignKey(Person, models.CASCADE, verbose_name='人员')
    date = models.DateField('日期')
    building = models.ForeignKey(Building, models.CASCADE, verbose_name='楼宇')
    room = models.CharField('房间号', max_length=100)
    purpose = models.CharField('事由', max_length=100)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)
    change_time = models.DateTimeField('修改时间', auto_now=True)
    approve1_time = models.DateTimeField('部门审核时间', null=True, blank=True)
    approve1_person = models.ForeignKey(Person, models.SET_NULL, related_name='approved_entries1', null=True, blank=True, verbose_name='部门审核人')
    approve1_decision = models.NullBooleanField('部门审核意见')
    approve2_time = models.DateTimeField('干事审核时间', null=True, blank=True)
    approve2_person = models.ForeignKey(Person, models.SET_NULL, related_name='approved_entries2', null=True, blank=True, verbose_name='干事审核人')
    approve2_decision = models.NullBooleanField('干事审核意见')
    approve3_time = models.DateTimeField('主管审核时间', null=True, blank=True)
    approve3_person = models.ForeignKey(Person, models.SET_NULL, related_name='approved_entries3', null=True, blank=True, verbose_name='主管审核人')
    approve3_decision = models.NullBooleanField('主管审核意见')

    class Meta:
        verbose_name = '进楼申请'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.person) + ' >' + str(self.building) + ' @' + str(self.date)
