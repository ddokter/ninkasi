from datetime import datetime
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory, HiddenInput
from django.forms.models import modelform_factory
from django.urls import reverse
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .base import CreateView, UpdateView, DetailView
from ..models.brew import Brew
from ..models.batch import Batch
from ..models.metaphase import MetaPhase
from ..models.malt import MaltMap, Malt, MaltProduct
from ..models.hop import Hop
from ..models.yeast import Yeast
from ..models.other import Other


class BrewDetailView(DetailView):

    """ Add phase vocab. TODO: could be a template_tag I guess """

    model = Brew
    can_log = True

    def nr_of_tasks(self):

        """ show nr of tasks open """

        return self.object.task.filter(status=0).count()

    def open_checks(self):

        return self.object.list_qualitychecks().filter(actual__isnull=True)

    def faulty_checks(self):

        for check in self.object.list_qualitychecks().filter(
                actual__isnull=False):

            if not check.is_ok:
                return False

        return True

    def phase_vocab(self):

        """ List phases defined for this system """

        return MetaPhase.objects.filter(parents__model="brew")


class BrewCreateView(CreateView):

    model = Brew

    def get_initial(self):

        """ Get initial form fields """

        if self.kwargs.get('batch'):
            return {'batch': Batch.objects.get(pk=self.kwargs['batch'])}

        return {}


class BrewUpdateView(UpdateView):

    model = Brew

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields['batch'].widget = HiddenInput()

        return form


class BrewImportPhasesView(DetailView):

    """ Get all brew phases from brewed beer """

    model = Brew

    @property
    def success_url(self):

        return reverse("view", kwargs={'pk': self.get_object().pk,
                                       'model': 'brew'})

    def get(self, request, *args, **kwargs):

        """ Shortcut to import of phases from recipe provided """

        if request.GET.get('recipe'):

            self.get_object().import_phases(request.GET['recipe'])
        else:
            messages.error(self.request, _("Recipe to import not provided."))

        return HttpResponseRedirect(self.success_url)


class BrewImportMaterialsView(DetailView):

    """ Get all brew materials from recipe """

    model = Brew
    template_name = "brew_importmaterials.html"

    @property
    def success_url(self):

        return reverse("view", kwargs={'pk': self.get_object().pk,
                                       'model': 'brew'})

    def list_to_malts(self):

        return Malt.objects.all()

    def list_to_hops(self):

        return Hop.objects.all()

    def list_to_yeasts(self):

        return Yeast.objects.all()

    def list_to_others(self):

        return Other.objects.all()

    def get_import_map(self):

        """ Create suggested mapping """

        import_map = {}
        recipe_id = self.request.GET['recipe']

        recipe = self.get_object().batch.beer.get_recipe(recipe_id)

        for ingredient in recipe.list_malts():

            ingredient.category = "malt"

            if MaltMap.objects.filter(from_malt=ingredient.name).exists():

                import_map[ingredient] = MaltMap.objects.get(
                    from_malt=ingredient.name).to_malt.id
            else:
                import_map[ingredient] = None

        for ingredient in recipe.list_hops():

            ingredient.category = "hop"

            if Hop.objects.filter(name=ingredient.name).exists():
                import_map[ingredient] = Hop.objects.get(
                    name=ingredient.name).id
            else:
                import_map[ingredient] = None

        for ingredient in recipe.list_yeasts():

            ingredient.category = "yeast"

            if Yeast.objects.filter(name=ingredient.name).exists():
                import_map[ingredient] = Yeast.objects.get(
                    name=ingredient.name).id
            else:
                import_map[ingredient] = None

        for ingredient in recipe.list_other():

            ingredient.category = "other"

            if Other.objects.filter(name=ingredient.name).exists():
                import_map[ingredient.name] = Other.objects.get(
                    name=ingredient.name)
            else:
                import_map[ingredient] = None

        return import_map

    def get(self, request, *args, **kwargs):

        """If the recipe is native, the ingredients can just be
        imported without conversion to local stuff."""

        recipe_id = self.request.GET['recipe']

        self.recipe = self.get_object().batch.beer.get_recipe(recipe_id)

        native = apps.get_model("ninkasi", "Recipe")

        if isinstance(self.recipe, native):

            brew = self.get_object()

            brew.brewmaterial_set.all().delete()

            for ingredient in self.recipe.list_ingredients():
                brew.brewmaterial_set.create(
                    amount=ingredient.amount,
                    unit=ingredient.unit,
                    material=ingredient.ingredient
                )

            return HttpResponseRedirect(self.success_url)
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        """ Map malts of remote recipe to Ninkasi base malts """

        brew = self.get_object()

        brew.brewmaterial_set.all().delete()

        for material in self.get_import_map():

            if request.POST.get(f"{imalt['name']}_new", None):

                if material.category == 'malt':

                    malt = Malt.objects.create(
                        name=request.POST[f"{imalt['name']}_new_malt"]
                    )
                    MaltMap.objects.create(
                        from_malt=imalt['name'], to_malt=malt
                    )

                    brew.brewmaterial_set.create(
                        amount=imalt['amount'],
                        unit=imalt['unit'],
                        material=malt
                    )

            elif request.POST.get(f"{imalt['name']}_to", None):

                to_malt = Malt.objects.get(
                    pk=int(request.POST[f"{imalt['name']}_to_malt"])
                )

                MaltMap.objects.update_or_create(
                    from_malt=imalt['name'],
                    to_malt=to_malt
                )
                brew.brewmaterial_set.create(
                    amount=imalt['amount'],
                    unit=imalt['unit'],
                    material=to_malt
                )

        return HttpResponseRedirect(self.success_url)


class BrewChecks(BrewDetailView):

    """Listing of qualitychecks related to this brew, generated by
    it's phases. """

    template_name = "brew_checks.html"

    @property
    def default_time(self):

        return datetime.now()

    @property
    def success_url(self):

        return reverse("brew_qualitychecks",
                       kwargs={'pk': self.get_object().pk})

    def list_qcs(self):

        """List all checks for this brew.

        """

        return self.get_object().list_qualitychecks()

    def post(self, request, *args, **kwargs):

        """ Set check values """

        brew = self.get_object()

        for qc in self.list_qcs():

            if request.POST.get(f"{qc.id}_value", None):
                qc.actual = request.POST.get(f"{qc.id}_value")
                qc.time = request.POST.get(f"{qc.id}_timestamp")
                qc.notes = request.POST.get(f"{qc.id}_notes")
                qc.save()

        return HttpResponseRedirect(self.success_url)


class BrewTasks(BrewDetailView):

    """ View on all tasks associated with this brew """

    template_name = "brew_tasks.html"

    def list_tasks(self):

        """ List all tasks for the brew """

        return self.object.task.all()


class BrewMeasurements(BrewDetailView):

    """ Show measurements for the brew """

    template_name = "brew_measurements.html"

    def list_measurements(self):

        return self.measurements.all()
