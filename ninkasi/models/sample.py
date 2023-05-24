from django.db import models
from django.utils.translation import gettext_lazy as _
from .batch import Batch
from .phase import Phase


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


class Sample(models.Model):

    """ Sample of any kind
    """

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    date = models.DateTimeField(_("Time"))
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(_("Quantity"),
                                        choices=Q_VOCAB
                                        )
    unit = models.SmallIntegerField(_("Unit"),
                                    choices=U_VOCAB)
    value = models.FloatField(_("Value"))

    def __str__(self):

        return (f"{self.batch} {self.date} {self.get_quantity_display()}"
                f" {self.get_unit_display()} {self.value}"
                )

    class Meta:

        app_label = "ninkasi"
