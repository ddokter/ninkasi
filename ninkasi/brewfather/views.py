from django.views.generic.detail import DetailView
from ninkasi.resource import ResourceRegistry


class RecipeView(DetailView):

    mode = "ro"
    template_name = "brewfather_recipe_detail.html"

    def get_object(self):

        res = ResourceRegistry.get_resource('recipe', 'bf')

        return res.get(self.kwargs['pk'])
