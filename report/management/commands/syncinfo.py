from django.core.management.base import BaseCommand

from ...models import Person


class Command(BaseCommand):
    help = 'Synchronize info with django.contrib.auth'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        count = 0
        for person in Person.objects.filter(user__isnull=False):
            user = person.user
            user.first_name = person.name
            user.is_staff = (
                person.can_contact.exists() or
                person.can_approve1.exists() or
                person.can_approve2.exists() or
                person.can_approve3.exists()
            ) or user.is_superuser
            if user.is_staff:
                print('Grant staff to {}: {} {} {} {}'.format(
                    person.name,
                    list(person.can_contact.all()),
                    list(person.can_approve1.all()),
                    list(person.can_approve2.all()),
                    list(person.can_approve3.all()),
                ))
            user.save(update_fields=('first_name', 'is_staff'))
            count += 1
        self.stdout.write(self.style.SUCCESS('{} synchronized'.format(count)))
