from django.db import models
from django.utils.translation import gettext_lazy as _
from .tank import Tank


class Batch(models.Model):

    """ One brew """

    nr = models.CharField(_("Nr"), max_length=100)
    beer = models.CharField(_("Beer"), max_length=100)
    volume = models.FloatField(_("Volume in liters"),
                               blank=True, null=True)
    tank = models.ManyToManyField(Tank, through="BatchTank")

    def __str__(self):

        return f"{self.beer} - #{self.nr}"

    def list_tanks(self):

        return self.batchtank_set.all()

    class Meta:

        app_label = "ninkasi"
        ordering = ["nr"]
        verbose_name_plural = _("Batches")


class BatchTank(models.Model):

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    date_from = models.DateTimeField(_("Date from"))
    date_to = models.DateTimeField(_("Date to"))
