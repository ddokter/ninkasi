""" Ninkasi app config module """

from django.apps import AppConfig, apps
from django.forms import widgets
from .resource import ResourceRegistry
from .milestones import (MilestoneRegistry, MilestoneProvider,
                         MilestoneProviderModel)
from .resource import ModelResource
from .utils import class_implements


class NinkasiConfig(AppConfig):

    """Ninkasi app config. Taking care of registries and some monkey
    patching."""

    name = 'ninkasi'

    def ready(self):

        """ App ready handler """

        # Monkey patch date/time inputs
        #
        widgets.DateTimeInput.input_type = 'datetime-local'
        widgets.DateInput.input_type = 'date'
        widgets.TimeInput.input_type = 'time'

        # Register model resources for style and recipes
        #
        style_model = apps.get_model("ninkasi", "style")

        ResourceRegistry.register("style", "django",
                                  ModelResource(style_model))

        recipe_model = apps.get_model("ninkasi", "recipe")

        ResourceRegistry.register("recipe", "django",
                                  ModelResource(recipe_model))

        # register milestone providers
        #
        for model_name, model in self.models.items():

            if class_implements(model, MilestoneProviderModel):

                MilestoneRegistry.register_model(model_name, model)

            elif class_implements(model, MilestoneProvider):

                MilestoneRegistry.register(model_name, model)
