from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import inlineformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from .base import CreateView, UpdateView, DetailView
from ..models.step import RecipeStep
from ..models.recipe import Recipe
from ..models.phase import Phase
from ninkasi.apps import PhaseRegistry


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

    model = Recipe

    def phase_vocab(self):

        """ List phases defned for this system """

        return PhaseRegistry.get_phases()


class RecipeCreateView(CreateView):

    model = Recipe


#  class RecipeUpdateView(FormSetMixin, UpdateView):
class RecipeUpdateView(UpdateView):

    model = Recipe


class RecipeAddPhaseView(DetailView):

    model = Recipe

    @property
    def success_url(self):

        obj = self.get_object()

        return reverse("view", kwargs={
            'pk': obj.pk,
            'model': 'recipe'})

    def get(self, *args, **kwargs):

        """ Shortcut to creation of phases """

        if kwargs.get('phase'):


            parent = self.get_object()
            phase = PhaseRegistry.get_phase(kwargs['phase'])

            order = 0

            try:
                order = parent.phase.last().order + 1
            except Exception:
                pass
            
            parent.phase.create(metaphase=phase.id, order=order)

        return HttpResponseRedirect(self.success_url)


class RecipeMovePhaseView(RecipeAddPhaseView):

    def get(self, request, *args, **kwargs):

        """ Shortcut to moving of phases """

        if kwargs.get('phase'):

            parent = self.get_object()

            parent.move(kwargs['phase'], request.GET.get('dir'))

        return HttpResponseRedirect(self.success_url)
