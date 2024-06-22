from django.views.generic.detail import DetailView
from ninkasi.resource import ResourceRegistry


class RecipeView(DetailView):

    mode = "ro"
    template_name = "brewfather_recipe_detail.html"
    ctype = "recipe"

    def get_object(self):

        """ Retrieve the actual object from the resource. """

        res = ResourceRegistry.get_resource('recipe', 'bf')

        return res.get(self.kwargs['pk'])
