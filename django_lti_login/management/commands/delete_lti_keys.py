from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from django_lti_login.models import LTIClient

class Command(BaseCommand):
    help = 'Delete a lti login key from the database'

    def add_arguments(self, parser):
        parser.add_argument('-k', '--key',
                            help="A key filter")
        parser.add_argument('-d', '--desc',
                            help="A description filter")

    def handle(self, *args, **options):
        key = options['key']
        desc = options['desc']

        qs = LTIClient.objects.all()
        if key:
            qs = qs.filter(key__startswith=key)
        if desc:
            qs = qs.filter(description__startswith=desc)

        objs = list(qs)
        amount = len(objs)

        if not amount:
            raise CommandError("No keys found")

        self.stdout.write(self.style.WARNING(
            "Listing {} keys about to be deleted".format(amount)
        ))

        for lticlient in objs:
            self.stdout.write(
                "-------\n"
                "   key: {c.key}\n"
                "  desc: {c.description}\n"
                .format(c=lticlient)
            )

        if not self.confirmation("Are you sure that you wan't to delete above keys?"):
            self.stdout.write(self.style.WARNING("Aborted."))
            return

        deleted = LTIClient.objects.filter(key__in=[o.key for o in objs]).delete()[0]

        if deleted == amount:
            self.stdout.write(self.style.SUCCESS(
                "Succesfully deleted all {} keys.".format(deleted)
            ))
        else:
            self.stdout.write(self.style.WARNING(
                "Succesfully deleted only {} keys out of requested {} keys".format(deleted, amount)
            ))

    def confirmation(self, message):
        msg = self.style.WARNING(message + " [yes/no]: ")
        msg2 = self.style.ERROR("Please answer yes or no: ")

        result = input(msg)
        while len(result) < 1 or result[0].lower() not in "yn":
            result = input(msg2)
        return result[0].lower() == "y"
