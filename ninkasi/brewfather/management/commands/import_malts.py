from django.core.management.base import BaseCommand
from django.conf import settings
from ninkasi.brewfather import api as bf


HELP = """Import BrewFather Malts
Usage: import_malts
"""


class Command(BaseCommand):

    def handle(self, *args, **options):

        if options['verbosity'] > 1:
            self.stdout.write("Calling BrewFather API")

        for ferm in bf.list_fermentables(limit=-1):

            print(f"{ferm['name']} {ferm['supplier']}")
