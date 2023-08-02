from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from .asset import Asset
from .step import Step
from .unit import Unit


class Brew(models.Model):

    """One brew. This boils down to one full brewing cycle on the
    brewhouse. One or more brews make up a batch.

    """

    batch = models.ForeignKey("Batch", on_delete=models.CASCADE)
    brewhouse = models.ForeignKey("Brewhouse", on_delete=models.CASCADE)
    date = models.DateTimeField(_("Time"))
    asset = models.ManyToManyField(Asset, through="BrewAsset", null=True,
                                   blank=True)
    step = models.ManyToManyField(Step, through="BrewStep")
    tank = models.ManyToManyField("Tank", through="BrewTransfer")
    sample = GenericRelation("Sample")

    def __str__(self):

        return f"{self.batch.nr} - {self.batch.recipe}"

    def list_assets(self):

        return self.brewasset_set.all()

    def list_steps(self):

        return self.brewstep_set.all()

    def list_transfers(self):

        return self.brewtransfer_set.all()

    def get_total_duration(self, unit='day'):

        """ TODO: use days or no """

        return (sum([step.get_duration() for step in self.step_set.all()]) /
                (60 * 24))

    @property
    def volume(self):

        """ The brew volume is the volume of the final transfer """

        if self.list_transfers().exists():
            return self.list_transfers().last().volume

        return 0

    class Meta:

        app_label = "ninkasi"
        ordering = ["batch__nr", "date"]
        verbose_name_plural = _("Brews")


class BrewTransfer(models.Model):

    """ Represent racking from one tank to the other """

    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
    tank = models.ForeignKey("Tank", on_delete=models.CASCADE)
    date = models.DateTimeField(_("Date from"))
    end_date = models.DateTimeField(_("Date to"), blank=True, null=True,
                                    editable=False)
    volume = models.SmallIntegerField(_("Volume"), blank=True, null=True)


    class Meta:

        app_label = "ninkasi"
        ordering = ["date"]


class BrewStep(models.Model):

    """ Represent racking from one tank to the other """

    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start time"))
    end_time = models.DateTimeField(_("End time"))

    @property
    def duration(self):

        """ Duration in minutes """

        return (self.end_time - self.start_time).seconds / 60

    class Meta:

        app_label = "ninkasi"
        ordering = ["start_time"]


class BrewAsset(models.Model):

    """Assets are related to a brew by a batchcode and an amount. The
    total batch assets are the sum of it's own assets and the brew
    assets.

    """

    amount = models.FloatField(_("Amount"))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    batchnr = models.CharField(_("Batch Nr"), max_length=100)

    @property
    def label(self):

        return _("Assets")

    def __str__(self):

        return "%s %s" % (self.asset, self.amount)
