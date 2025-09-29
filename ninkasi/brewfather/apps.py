from django.apps import AppConfig
from ninkasi.modules import ModuleRegistry


class BrewFatherModule():

    name = "ninkasi.brewfather"
    title = "BrewFather"
    href = "#"


class BrewFatherConfig(AppConfig):

    name = "ninkasi.brewfather"
    verbose_name = "Brewfather Frontend App"

    def ready(self):

        module = BrewFatherModule()

        ModuleRegistry.register(module)
