""" Hold batch model """

from random import choice
from datetime import timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .tank import Tank
from .asset import Asset
from .unit import Unit
from .step import Step


class Batch(models.Model):

    """ One production for a given recipe. """

    nr = models.CharField(_("Nr"), max_length=100, unique=True)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    asset = models.ManyToManyField(Asset, through="BatchAsset")
    tank = models.ManyToManyField(Tank, through="Transfer")
    step = models.ManyToManyField(Step, through="BatchStep")
    sample = GenericRelation("Sample")
    deliverydate = models.DateTimeField(_("Delivery date"),
                                        null=True, blank=True)
    color = models.CharField(_("Graph color"), max_length=7,
                             null=True, blank=True)

    @property
    def volume(self):

        """Total batch volume, i.e. sum of brew volumes """

        return sum([brew.volume for brew in self.list_brews()])

    def __str__(self):

        return f"{self.recipe.name} - #{self.nr}"

    def get_status(self):

        """ Return a list of problems, if any.  """

        problems = []

        #if not self.list_steps().exists():
        #    problems.append(("danger", _("No steps defined in the batch")))

        #if self.list_steps().count() != self.recipe.list_steps().count():
        #    problems.append(("warning", _("Steps of batch and recipe differ")))

        return problems

    def list_brews(self):

        return self.brew_set.all()

    def list_steps(self):

        return self.batchstep_set.all()

    def list_assets(self):

        """ List all assets, also of sub brews """
        
        batch_assets = self.batchasset_set.all()

        for brew in self.list_brews():
            batch_assets = batch_assets.union(brew.list_assets())

        return batch_assets
            
    def list_transfers(self):

        return self.transfer_set.all()

    def list_samples(self):

        """ samples may be taken from a batch. List them. """

        return self.sample_set.all()

    def get_color(self):

        """Return a random color from the given palette"""

        return self.color or choice([
            '#d9ed92', '#b5e48c', '#99d98c', '#76c893', '#52b69a',
            '#34a0a4', '#168aad', '#1a759f', '#1e6091', '#184e77'])

    @property
    def start_date(self):

        """ The start date is inferred from the first brew """

        if self.list_brews().exists():

            return self.list_brews().first().date

        return None

    @property
    def end_date_planned(self):

        """ The end date according to the start date plus the number
        of days specified in the recipe """

        if self.start_date:

            return self.start_date + timedelta(
                days=self.recipe.get_total_duration())

        return None

    @property
    def end_date_expected(self):

        """ End date calculated from start date and steps """

        if self.start_date:

            return self.start_date + timedelta(
                days=self.get_total_duration())

        return None

    def get_total_duration(self, unit='day'):

        """ TODO: use days or no """

        return (sum([step.get_duration() for step in self.step.all()]) /
                (60 * 24))

    def get_current_step(self):

        """ Return the step the batch is in currently """

    class Meta:

        app_label = "ninkasi"
        ordering = ["nr"]
        verbose_name_plural = _("Batches")


class Transfer(models.Model):

    """ Represent racking from one tank to the other """

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    #origin = GenericForeignKey("content_type", "object_id")
    #content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #object_id = models.PositiveIntegerField()
    date = models.DateTimeField(_("Date from"))
    end_date = models.DateTimeField(_("Date to"), blank=True, null=True,
                                    editable=False)
    volume = models.SmallIntegerField(_("Volume"), blank=True, null=True)

        
    class Meta:

        app_label = "ninkasi"
        ordering = ["date"]


class BatchStep(models.Model):

    """ Represent racking from one tank to the other """

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    # step = GenericRelation(Step, on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start time"))
    end_time = models.DateTimeField(_("End time"))

    class Meta:

        app_label = "ninkasi"
        ordering = ["start_time"]


class BatchAsset(models.Model):

    # TODO: make sure that there is a conversion from given unit to
    # ingredient's default unit

    amount = models.FloatField(_("Amount"))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    batchnr = models.CharField(_("Batch Nr"), max_length=100)

    @property
    def label(self):

        return _("Assets")

    def __str__(self):

        return f"{self.asset} {self.amount}"
