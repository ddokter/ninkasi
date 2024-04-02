from django.apps import AppConfig
from ninkasi.resource import ResourceRegistry
from .resource import RecipeResource


class BrewFatherConfig(AppConfig):

    name = "ninkasi.brewfather"
    verbose_name = "Brewfather Frontend App"

    def ready(self):

        ResourceRegistry.register("recipe", "bf", RecipeResource())
