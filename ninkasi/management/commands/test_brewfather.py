from django.core.management.base import BaseCommand
from django.conf import settings
from ninkasi.brewfather import api as bf


HELP = """Test BrewFather API
Usage: test_brewfather --action=<str>

Options:
"""

class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument("--id", dest="_id", nargs="?")
        parser.add_argument('--action', dest='action',
                            help='Specify controller action')

    def handle(self, *args, **options):

        if options['verbosity'] > 1:
            self.stdout.write("Calling BrewFather API")

        if options['_id']:
            res = getattr(bf, options['action'])(options['_id'])
        else:
            res = getattr(bf, options['action'])()

        if options['verbosity'] > 2:
            self.stdout.write(res.text)

        # data = json.loads(res.text)

        self.stdout.write(str(res))
