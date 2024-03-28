from ninkasi.models.recipe import get_recipe_model
from base import BaseDetailView


class RecipeView(BaseDetailView):

    @property
    def model(self):

        return get_recipe_model()

    def get_queryset(self):

        return get_recipe_model().objects.all()
