from django.apps import apps
from django.db import models
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):

    """ Simple Brand model

    """

    name = models.CharField(_("Name"), null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):

        return self.name

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
