from django.db import models

from report.models import Person


class Post(models.Model):
    code = models.CharField('代码', max_length=32, unique=True)
    description = models.CharField('描述', max_length=100)
    members = models.ManyToManyField(Person, verbose_name='成员')

    class Meta:
        verbose_name = '岗位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.description


class Task(models.Model):
    code = models.CharField('代码', max_length=32, unique=True)
    description = models.CharField('描述', max_length=100)
    begin_date = models.DateField('开始日期')
    end_date = models.DateField('结束日期')
    deadline = models.DateTimeField('提交截止时间')

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.description


class Report(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, verbose_name='岗位')
    task = models.ForeignKey(Task, models.CASCADE, verbose_name='任务')
    content = models.TextField('内容', blank=True)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)
    change_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '报告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{task}*{post}'.format(
            task=self.task,
            post=self.post,
        )


def report_attachment_path(instance, filename):
    report = instance.report
    return 'uawg/{task_code}/{post_code}/{filename}'.format(
        task_code=report.task.code,
        post_code=report.post.code,
        filename=filename,
    )

class ReportAttachment(models.Model):
    report = models.ForeignKey(Report, models.CASCADE, verbose_name='报告')
    file = models.FileField('文件', upload_to=report_attachment_path)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)
    change_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '报告附件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.file.name
