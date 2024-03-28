from django.core.management.base import BaseCommand
from django.conf import settings
from ninkasi.bjcp import list_styles
from ninkasi.models.style import Style


HELP = """Import styles from BJCP API
Usage: import_bjcp_styles

Options:
  --sim Simulate action only
"""

class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('--sim', dest='sim',
                            help='Simulate only')

    def handle(self, *args, **options):

        if options['verbosity'] > 1:
            self.stdout.write("Calling BJCP API")

        res = list_styles()

        if options['verbosity'] > 2:
            self.stdout.write(str(res))

        for style in res['beerStyles']['data']:

            data = style['attributes']

            if not options['sim']:
                Style.objects.update_or_create(
                    name=data['name'],
                    defaults={"description": data['comments'],
                              "color": f"{ data['srmMin'] },{ data['srmMax'] }",
                              "source": "bjcp"}
                )
            else:
                self.stdout.write(f"Found style { data['name'] }")
