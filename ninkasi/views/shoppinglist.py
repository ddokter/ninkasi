from datetime import datetime
from django.views.generic import TemplateView
from ..models.batch import Batch


class ShoppingListView(TemplateView):

    """Generate a shopping list for planned batches, given a specific
    date.

    """

    template_name = "shoppinglist.html"

    def get_list(self):

        """ Generate the list of needed stuff """

        today = datetime.now()

        materials = []

        _filter = {'date__gt': today}

        if self.request.GET.get('date', None):

            date = datetime.strptime(self.request.GET.get('date'),
                                     "%Y-%m-%d").date()
            _filter['date__lte'] = date

        for batch in Batch.objects.filter(**_filter):

            for material in batch.list_batchmaterials():

                materials.append(material)

        return materials
