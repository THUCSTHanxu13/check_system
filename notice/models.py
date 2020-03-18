from django.db import models

from report.models import Person


class Notice(models.Model):
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    post_time = models.DateTimeField('发布时间')
    source = models.CharField('来源', max_length=100)
    source_url = models.URLField('原始链接', blank=True)
    published = models.BooleanField('是否公布')
    to_ack = models.BooleanField('是否需要确认', default=False)
    marked = models.BooleanField('重要标记', default=False)
    read_count = models.IntegerField('阅读次数', default=0)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)
    acked_persons = models.ManyToManyField(
        Person, through='Ack', related_name='acked_notices',
        verbose_name='已确认人员',
    )

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Ack(models.Model):
    notice = models.ForeignKey(Notice, models.CASCADE, verbose_name='通知')
    person = models.ForeignKey(Person, models.CASCADE, verbose_name='人员')
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '确认'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} * {}'.format(self.notice, self.person)


def notice_attachment_path(instance, filename):
    return 'notice/{notice_id}/{filename}'.format(
        notice_id=instance.notice.id,
        filename=filename,
    )

class Attachment(models.Model):
    notice = models.ForeignKey(Notice, models.CASCADE, verbose_name='通知')
    file = models.FileField('文件', upload_to=notice_attachment_path)
    weight = models.IntegerField('权重', default=0, help_text='决定附件排序，越大越靠前。')
    add_time = models.DateTimeField('添加时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = verbose_name
        ordering = ('-weight', 'file')

    def basename(self):
        pos = self.file.name.rfind('/')
        return self.file.name[pos + 1:]

    def __str__(self):
        return str(self.file)
