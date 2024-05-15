from django.db import models
from django.utils.translation import gettext_lazy as _


class Container(models.Model):

    """ Anything that can hold a batch of beer. May be a brewhouse,
    but also a tank, like CCT or BBT. The container is used to define
    where a specific batch is. """

    name = models.CharField(_("Name"), max_length=100)
    volume = models.FloatField()

    maintenance_schema = models.ManyToManyField("Task", null=True, blank=True)

    def __str__(self):

        return self.name

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]
        abstract = True
