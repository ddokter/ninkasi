from random import choice
from datetime import datetime
from django.views.generic import TemplateView
from django.utils import timezone
from ..models.tank import Tank
from ..models.brewhouse import Brewhouse
from ..utils import get_model_name
from .calendar import Calendar


class PlannerView(TemplateView, Calendar):

    """The planner view provides a monthly overview of tanks,
    brewhouses and their availability, based on scheduled batches.

    """

    template_name = "planner.html"

    def get_color(self):

        """Return a random color from the given palette
        """

        # TODO: make color a permanent feature of the batch somehow

        return choice([
            '#d9ed92', '#b5e48c', '#99d98c', '#76c893', '#52b69a',
            '#34a0a4', '#168aad', '#1a759f', '#1e6091', '#184e77'])

    def list_tanks(self):

        """ Return list of all tanks in the brewery """

        return Tank.objects.all()

    def get_data(self):

        """ Generate data for calendar. Loop over tanks and brewhouses,
        and display the calendar. """

        batches = {}
        tanks = {}

        for tank in list(self.list_tanks()) + list(self.list_brewhouses()):

            tankdata = {}

            for mday in self.month['days']:

                day = datetime(self.month['year'], self.month['month'], mday,
                               tzinfo=timezone.get_current_timezone())

                batch = tank.content(day)

                # Get the actual batch, in case the content of the
                # tank is a 'brew'
                #
                batch = self.get_batch(batch)

                if batch and not batch in batches:
                    batches[batch] = self.get_color()

                tankdata[mday] = (batch, batches.get(batch, None))

            tanks[tank] = tankdata

        return (tanks, batches)

    def list_brewhouses(self):

        """ Return a list of all brewhouses in the system """

        return Brewhouse.objects.all()

    def get_batch(self, thing):

        if get_model_name(thing) == "batch":
            return thing
        elif get_model_name(thing) == "brew":
            return thing.batch
        else:
            return None
