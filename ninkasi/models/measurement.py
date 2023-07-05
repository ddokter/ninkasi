from django.db import models
from django.utils.translation import gettext_lazy as _
from .sample import Sample


Q_VOCAB = [
    (0, _("Acidity")),
    (1, _("DO")),
    (2, _("Gravity")),
    (3, _("CO2")),
    (4, _("FAN"))
]


U_VOCAB = [
    (0, "Ph"),
    (1, "PPM"),
    (2, "SG")
]


class Measurement(models.Model):

    """ Measurement of any kind
    """

    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(_("Quantity"),
                                        choices=Q_VOCAB)
    unit = models.SmallIntegerField(_("Unit"),
                                    choices=U_VOCAB)
    value = models.FloatField(_("Value"))

    def __str__(self):

        return (f"{self.sample} {self.get_quantity_display()}"
                f" {self.get_unit_display()} {self.value}")

    @property
    def label(self):
    
        return _("Measurements")
    
    class Meta:
        
        app_label = "ninkasi"
