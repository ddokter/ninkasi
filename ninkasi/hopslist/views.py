from django.views.generic.detail import DetailView
from ninkasi.resource import ResourceRegistry


class HopDetailView(DetailView):

    mode = "ro"
    template_name = "hopslist_hop_detail.html"
    ctype = "hop"

    def get_object(self):

        """ Retrieve the actual object from the resource. """

        res = ResourceRegistry.get_resource('hop', 'hopslist')

        return res.get(self.kwargs['pk'])
