import csv
import datetime

from django.core.management.base import BaseCommand

from ...models import Person, Organization


class Command(BaseCommand):
    help = 'Import data'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', nargs=1)

    def handle(self, *args, **options):
        num_created = 0
        num_updated = 0
        with open(options['csvfile'][0]) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                idnum = row['工作证号']
                name = row['姓名']
                department_name = row['所在单位']
                department_code = row['单位代码']
                branch_name = row['所在部门']
                department, _ = Organization.objects.get_or_create(code=department_code, defaults={'name': department_name})
                if branch_name == department_name:
                    affiliation = department
                else:
                    branch, _ = Organization.objects.get_or_create(name=branch_name, defaults={'parent': department})
                    affiliation = branch
                category = row['人员类别']
                if category == '离退休':
                    category = '离退'
                elif name.isascii():
                    category = '外籍'
                else:
                    category = '内地'
                phone = row['联系电话']
                if len(phone) == 8:
                    phone = '010' + phone
                return_date = row['返京日期或计划返京日期']
                if return_date:
                    return_date = datetime.strptime(return_date, '%Y-%m-%d')
                else:
                    return_date = None
                _, created = Person.objects.update_or_create(
                    idnum=idnum,
                    defaults={
                        'name': name,
                        'affiliation': affiliation,
                        'category': category,
                        'phone': phone,
                        'return_date': return_date,
                        'remark': row['问题与意见'],
                    },
                )
                if created:
                    num_created += 1
                else:
                    num_updated += 1
        self.stdout.write(self.style.SUCCESS('{} created, {} updated'.format(num_created, num_updated)))
