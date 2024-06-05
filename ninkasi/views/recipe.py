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

        """ List phases defned for this system """

        return MetaPhase.objects.filter(parents__model="recipe")


class RecipeListingView(ListingView):

    """ Override base listing to show all resources for recipe's

    """

    model = Recipe

    def list_items(self):

        """ Fetch all recipe's from all resources """

        recipes = []

        for resource in ResourceRegistry.get_resources('recipe'):

            recipes.extend(resource.list())

        return recipes
