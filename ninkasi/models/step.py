from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .phase import Phase


DURATION_VOCAB = [
    (0, _("Minute")),
    (1, _("Hour")),
    (2, _("Day")),
]

DURATION_TO_MINUTES = [1, 60, 60 * 24]


class Step(models.Model):

    """ Step in the scheme for a recipe, batch or brew.
    """

    parent = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    temperature = models.FloatField(_("Temperature"))
    duration = models.FloatField(_("Duration"))
    duration_unit = models.SmallIntegerField(_("Duration unit"),
                                             choices=DURATION_VOCAB)

    def __str__(self):

        return f"{self.phase} - {self.temperature}°C"

    def get_duration(self):

        """ Get the duration in minutes """

        return self.duration * DURATION_TO_MINUTES[self.duration_unit]

    class Meta:

        app_label = "ninkasi"
