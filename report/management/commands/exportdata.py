from django.core.management.base import BaseCommand

from report.models import Person
from report.utils import export_as_csv


class Command(BaseCommand):
    help = 'Export data'

    def handle(self, *args, **options):
        export_as_csv(Person.objects.all(), self.stdout)
