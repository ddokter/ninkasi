from django.apps import AppConfig
from ninkasi.resource import ResourceRegistry
# from .resource import HopResource


class HopslistConfig(AppConfig):

    name = "ninkasi.hopslist"
    verbose_name = "Hoplist Frontend App"

    def ready(self):

        # ResourceRegistry.register("hop", "hopslist", HopResource())
        pass
