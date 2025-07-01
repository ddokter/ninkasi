from django.db import models
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):

    """ Brand or producer.

    """

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):

        return self.name

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
