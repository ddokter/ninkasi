""" Beer view overrides """

from django import forms
from ..models.beer import Beer, list_recipes, list_styles
from .base import CreateView, UpdateView


class URNSelect(forms.Select):

    """ Make sure the value is formatted to the URN, to enable select of
    set value """

    def format_value(self, value):

        """ Format for display in widget """

        try:
            return [value.urn]
        except AttributeError:
            return []


class URNSelectMultiple(forms.SelectMultiple):

    """ Make sure the value is formatted to the URN, to enable select of
    set value """

    def format_value(self, value):

        """ Format for display in widget """

        try:
            return [val.urn for val in value if getattr(val, "urn")]
        except TypeError:
            return []


class BeerForm(forms.ModelForm):

    """ Recipes field should be multiple choice. """

    recipes = forms.MultipleChoiceField(choices=list_recipes,
                                        required=False,
                                        widget=URNSelectMultiple)

    style = forms.TypedChoiceField(choices=list_styles, widget=URNSelect)

    class Meta:
        fields = "__all__"
        model = Beer


class BeerCreateView(CreateView):

    """ Override to enable custom form """

    fields = None
    model = Beer
    form_class = BeerForm


class BeerUpdateView(UpdateView):

    """ Override to enable custom form """

    fields = None
    model = Beer
    form_class = BeerForm
