from django.db import models
from report.models import Person

class PartyDocument(models.Model):
    person = models.ForeignKey(Person, models.CASCADE, verbose_name='人员')
    uid = models.CharField('系统随机编码', blank = False, max_length=250)
    upload_name = models.CharField('上传文件路径', blank=True, max_length=250)
    download_name = models.CharField('docx格式评估结果路径', blank=True, max_length=250)
    json_name = models.CharField('json格式评估结果路径', blank=True, max_length=250)
    completion_flag = models.BooleanField('是否完成评测', default = False)

    class Meta:
        verbose_name = '党员材料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.person) + ' @' + str(self.date)

