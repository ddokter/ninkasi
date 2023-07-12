from datetime import datetime, date
from calendar import monthrange
from django.views.generic import TemplateView
from ..models.tank import Tank
from ..models.brewhouse import Brewhouse


class TankPlannerView(TemplateView):

    template_name = "tankplanner.html"

    def list_tanks(self):

        return Tank.objects.all()

    def list_brewhouses(self):

        return Brewhouse.objects.all()

    @property
    def month(self):

        """ Return current month """

        if self.request.GET.get('go', None):

            year, month = self.request.GET['go'].split('-')

            now = date(int(year), int(month), 1)
        else:
            now = datetime.now()

        if now.month == 12:
            _next = date(now.year + 1, 1, 1)
        else:
            _next = date(now.year, now.month + 1, 1)

        if now.month == 1:
            _prev = date(now.year - 1, 12, 1)
        else:
            _prev = date(now.year, now.month - 1, 1)


        return {
            'title': now.strftime("%B"),
            'days': range(1, monthrange(now.year, now.month)[1] + 1),
            'next': _next.strftime("%Y-%m"),
            'prev': _prev.strftime("%Y-%m"),
            'month': now.month,
            'year': now.year
            }
