from django.core.management.base import BaseCommand

from django_lti_login.models import LTIClient

class Command(BaseCommand):
    help = 'List all lti login keys in database'

    def add_arguments(self, parser):
        parser.add_argument('-k', '--key',
                            help="Key filter")
        parser.add_argument('-d', '--desc',
                            help="Description filter")

    def handle(self, *args, **options):
        key = options['key']
        desc = options['desc']

        qs = LTIClient.objects.all()
        if key:
            qs = qs.filter(key__startswith=key)
        if desc:
            qs = qs.filter(description__startswith=desc)

        amount = qs.count()
        if amount:
            self.stdout.write(self.style.SUCCESS(
                "Printing list of {} keys".format(amount)
            ))

            for lticlient in qs:
                self.stdout.write(
                    "-------\n"
                    "   key: {c.key}\n"
                    "secret: {c.secret}\n"
                    "  desc: {c.description}\n"
                    .format(c=lticlient)
                )
            self.stdout.write("-------")
        else:
            self.stdout.write(self.style.WARNING(
                "No keys found from database"
            ))
