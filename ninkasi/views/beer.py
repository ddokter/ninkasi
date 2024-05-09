from django import forms
from ..models.beer import Beer, list_recipes
from .base import CreateView


class BeerForm(forms.ModelForm):

    recipes = forms.MultipleChoiceField(choices=list_recipes)

    class Meta:
        fields = "__all__"
        model = Beer


class BeerCreateView(CreateView):

    model = Beer
    form_class = BeerForm
