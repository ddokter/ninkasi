from django.apps import AppConfig
from ninkasi.resource import ResourceRegistry
from .resource import StyleResource


class BJCPConfig(AppConfig):

    name = "ninkasi.bjcp"
    verbose_name = "BJCP App"

    def ready(self):

        ResourceRegistry.register("style", "bjcp", StyleResource())
