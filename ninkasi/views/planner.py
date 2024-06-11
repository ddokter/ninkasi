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

            for day in self.month['days']:

                batch = tank.content(day)

                # Get the actual batch, in case the content of the
                # tank is a 'brew'
                #
                batch = self.get_batch(batch)

                if batch and batch not in batches:
                    batches[batch] = batch.color

                tankdata[day] = (batch, batches.get(batch, None))

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
