from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


PHASE_VOCAB = [
    (0, _("Mash")),
    (1, _("Fermentation")),
    (2, _("Lagering")),
]

PHASE_VOCAB_DICT = dict(PHASE_VOCAB)

DURATION_VOCAB = [
    (0, _("Minute")),
    (1, _("Hour")),
    (2, _("Day")),
]


class Step(models.Model):

    """ Step in the scheme for a recipe, batch or brew.
    """

    parent = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    
    phase = models.SmallIntegerField(_("Phase"), choices=PHASE_VOCAB)
    temperature = models.FloatField(_("Temperature"))
    duration = models.FloatField(_("Duration"))
    duration_unit = models.SmallIntegerField(_("Duration unit"),
                                             choices=DURATION_VOCAB)

    def __str__(self):

        return (f"{self.phase_label} - {self.temperature}°C")

    @property
    def phase_label(self):

        return PHASE_VOCAB_DICT[self.phase]

    @property
    def label(self):

        return _("Steps")

    class Meta:

        app_label = "ninkasi"
