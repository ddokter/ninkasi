from django.views.generic.detail import DetailView
from ninkasi.resource import ResourceRegistry


class StyleView(DetailView):

    mode = "ro"
    template_name = "bjcp_style_detail.html"
    ctype = "style"

    def get_object(self):

        """ Retrieve the actual object from the resource. """

        res = ResourceRegistry.get_resource('style', 'bjcp')

        return res.get(self.kwargs['pk'])
