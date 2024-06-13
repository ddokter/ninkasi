""" Measurement model definition """

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Measurement(models.Model):

    """ Measurement of any kind
    """

    parent = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    time = models.DateTimeField(_("Time"))
    quantity = models.ForeignKey("Quantity", on_delete=models.CASCADE)
    value = models.FloatField()
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)
    notes = models.TextField(_("Notes"), max_length=200, null=True,
                             blank=True)

    def __str__(self):

        return f"{self.quantity}: {self.value} { self.unit }"

    class Meta:

        app_label = "ninkasi"
        ordering = ['time']
