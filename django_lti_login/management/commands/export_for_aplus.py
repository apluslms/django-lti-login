import json

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django_lti_login.models import LTIClient


class Command(BaseCommand):
    help = "Exports a lti login key for A+"

    def add_arguments(self, parser):
        parser.add_argument('-k', '--key',
                            required=True,
                            help="The key to export")
        parser.add_argument('-l', '--label',
                            required=True,
                            help="Label for A+")
        parser.add_argument('-i', '--icon',
                            help="Menu icon name for A+")
        parser.add_argument('-b', '--base',
                            required=True,
                            help="Url base address")
        parser.add_argument('-u', '--url',
                            default='lti_login',
                            help="Url name for building reverse url (default: lti_login)")
        parser.add_argument('-f', '--file',
                            help="File to write the json data (default: stdout)")

    def handle(self, *args, **options):
        key = options['key']

        try:
            obj = LTIClient.objects.get(key=key)
        except LTIClient.DoesNotExist:
            raise CommandError("Could not find a LTIClient with key '{}'.".format(key))


        base = options['base'].rstrip('/')
        url = base + reverse(options['url'])

        data = {
            'key': obj.key,
            'secret': obj.secret,
            'label': options['label'],
            'url': url,
        }

        if options['icon']:
            data['icon'] = options['icon']

        if options['file']:
            with open(options['file'], 'w') as f:
                json.dump(data, f)
            self.stdout.write(self.style.SUCCESS("Successfully exported a lti info to '{}'".format(options['file'])))
        else:
            self.stdout.write(json.dumps(data))
