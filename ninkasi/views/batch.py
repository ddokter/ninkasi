import datetime
from random import choice
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory, Form, Select
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .base import CreateView, UpdateView, DetailView
from ..models.batch import Batch
from ..models.beer import Beer
from ..models.phase import Phase
from ..models.brewhouse import Brewhouse
from ..utils import get_model_name


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        # form.fields['color'].widget = ColorInput()

        for field in ['tank', 'material']:
            form.fields.pop(field)

        return form

    @property
    def formsets(self):

        factory1 = inlineformset_factory(
            Batch, Batch.material.through, exclude=[])

        factory2 = inlineformset_factory(
            Batch, Batch.tank.through, exclude=[])

        #factory2 = generic_inlineformset_factory(
        #    BatchStep, exclude=[],
            #widgets={'start_time': DateTimeInput(),
            #         'end_time': DateTimeInput()
            #         }
        #)

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        return [factory1(**kwargs), factory2(**kwargs)]

    def form_valid(self, form):

        """ Check the form and all formsets """

        self.object = form.save()

        for _formset in self.formsets:
            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class BatchCreateView(FormSetMixin, CreateView):

    model = Batch

    def get_initial(self):

        """ Batches may be created with an initial beer """

        if self.kwargs.get('beer'):
            return {'beer': Beer.objects.get(pk=self.kwargs['beer'])}

        return {}


class BatchUpdateView(FormSetMixin, UpdateView):

    model = Batch


class BatchDetailView(DetailView):

    model = Batch

    _color = None

    """ Provide the date range for this batch, so we can display
    a calendar for the containers """

    def get_calendar(self):

        """ Create date range from start to projected end,
        also provide a header for years and months.

        """

        _from = self.object.start_date
        _to = self.object.delivery_date

        dates = []
        months = {}
        years = {}

        if not (_from and _to):
            return dates

        while _from <= _to:
            dates.append(_from)

            if _from.month not in months:
                months[_from.month] = 1
            else:
                months[_from.month] += 1

            if _from.year not in years:
                years[_from.year] = 1
            else:
                years[_from.year] += 1

            _from += datetime.timedelta(days=1)

        return {"years": years.items(), "months": months.items(), "days":dates}

    def phase_vocab(self):

        """ List phases defned for this system """

        return Phase.objects.all()

    def list_tanks(self):

        return self.object.list_tanks()

    def list_brewhouses(self):

        return set(brew.brewhouse for brew in self.object.list_brews())

    def list_recipes(self):

        """ List possible recipes for this batch """

        return self.object.beer.recipes

    def get_color(self):

        """Return a random color from the given palette
        """

        if not self._color:

            self._color = choice([
                '#d9ed92', '#b5e48c', '#99d98c', '#76c893', '#52b69a',
                '#34a0a4', '#168aad', '#1a759f', '#1e6091', '#184e77'])

        return self._color

    def get_batch(self, thing):

        # TODO: dry!

        if get_model_name(thing) == "batch":
            return thing
        elif get_model_name(thing) == "brew":
            return thing.batch
        else:
            return None

    def get_tank_data(self):

        """ Fill tank/content data """

        tanks = {}

        days = self.get_calendar()["days"]

        unspecified = [1] * len(days)

        for tank in list(self.list_tanks()) + list(self.list_brewhouses()):

            tanks[tank] = []

            for day in days:

                batch = tank.content(day)

                batch = self.get_batch(batch)

                if batch == self.object:
                    tanks[tank].append(1)
                    unspecified[days.index(day)] = 0
                else:
                    tanks[tank].append(0)

        # Fill up Unspecified!
        #
        tanks['Unspecified'] = unspecified

        return tanks


class BatchImportPhasesView(BatchDetailView):

    @property
    def success_url(self):

        return reverse("view", kwargs={'pk': self.get_object().pk,
                                       'model': 'batch'})

    def get(self, request, *args, **kwargs):

        """ Shortcut to import of phases from recipe provided """

        if request.GET.get('recipe'):

            self.get_object().import_phases(request.GET['recipe'])
        else:
            messages.error(self.request, _("Recipe to import not provided."))

        return HttpResponseRedirect(self.success_url)
