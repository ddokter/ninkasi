from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from .asset import Asset
from .step import Step


class Brew(models.Model):

    """One brew. This boils down to one full brewing cycle on the
    brewhouse. One or more brews make up a batch.

    """

    batch = models.ForeignKey("Batch", on_delete=models.CASCADE)
    date = models.DateTimeField(_("Time"))
    volume = models.FloatField(_("Volume in liters"))
    asset = models.ManyToManyField(Asset, through="BrewAsset", null=True,
                                   blank=True)
    step = models.ManyToManyField(Step, null=True, blank=True)
    sample = GenericRelation("Sample")

    def __str__(self):

        return f"{self.batch.nr} - {self.batch.recipe}"

    def list_assets(self):

        return self.brewasset_set.all()

    class Meta:

        app_label = "ninkasi"
        ordering = ["batch__nr"]
        verbose_name_plural = _("Brews")


class BrewAsset(models.Model):

    """Assets are related to a brew by a batchcode and an amount. The
    total batch assets are the sum of it's own assets and the brew
    assets.

    """

    amount = models.FloatField(_("Amount"))
    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    batchnr = models.CharField(_("Batch Nr"), max_length=100)

    @property
    def label(self):

        return _("Assets")

    def __str__(self):

        return "%s %s" % (self.asset, self.amount)
