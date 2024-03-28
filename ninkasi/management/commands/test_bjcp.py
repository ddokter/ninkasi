from django.core.management.base import BaseCommand
from django.conf import settings
from ninkasi.bjcp import list_styles


HELP = """Test BJCP API
Usage: test_bjcp --action=<str>

Options:
"""

class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('--action', dest='action',
                            help='Specify controller action')

    def handle(self, *args, **options):

        if options['verbosity'] > 1:
            self.stdout.write("Calling BJCP API")

        res = list_styles()

        if options['verbosity'] > 2:
            self.stdout.write(str(res))

        # data = json.loads(res.text)

        self.stdout.write(str(res))
