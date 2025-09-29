from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import inlineformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib import messages
from ninkasi.resource import ResourceRegistry
from .base import DetailView, ListingView
from ..models.recipe import Recipe
from ..models.metaphase import MetaPhase


class RecipeDetailView(DetailView):

    model = Recipe

    def phase_vocab(self):

        """ List phases defined for this system """

        return MetaPhase.objects.filter(parents__model="recipe")
