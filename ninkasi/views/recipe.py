from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from .base import CreateView, UpdateView, DetailView
from ..models.recipe import get_recipe_model
from ..models.step import RecipeStep
from ..models.phase import Phase


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields.pop('ingredient')

        return form

    @property
    def formsets(self):

        #factory1 = inlineformset_factory(
        #    Recipe, Recipe.ingredient.through, exclude=[]
        #)

        factory2 = generic_inlineformset_factory(
            RecipeStep, exclude=[]
        )

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        return [factory1(**kwargs), factory2(**kwargs)]

    def form_valid(self, form):

        self.object = form.save()

        for _formset in self.formsets:

            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class RecipeView(DetailView):

    @property
    def model(self):

        return get_recipe_model()

    def get_queryset(self):

        return get_recipe_model().objects.all()

    def phase_vocab(self):

        """ List phases defned for this system """

        return Phase.objects.all()    


class RecipeCreateView(CreateView):

    @property
    def model(self):

        return get_recipe_model()


#  class RecipeUpdateView(FormSetMixin, UpdateView):
class RecipeUpdateView(UpdateView):

    @property
    def model(self):

        return get_recipe_model()
