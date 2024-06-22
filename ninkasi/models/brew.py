"""Brew model and related models for m2m relations."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from ..ordered import OrderedContainer
from .material import Material, ParentedMaterial
from ..milestones import MilestoneProviderModel
from ..duration import Duration
from .fields import DurationField


class Brew(models.Model, OrderedContainer, MilestoneProviderModel):

    """One brew. This boils down to one full brewing cycle on the
    brewhouse. One or more brews make up a batch. The Brew consists of
    phases, phases consist of steps. Recipe for a brew is inherited
    from the batch, but may be adjusted on the brew.

    """

    batch = models.ForeignKey("Batch", on_delete=models.CASCADE)
    brewhouse = models.ForeignKey("Brewhouse", on_delete=models.CASCADE)
    date = models.DateTimeField(_("Time"))
    material = models.ManyToManyField(Material, through="BrewMaterial")

    phase = GenericRelation("Phase")
    measurement = GenericRelation("Measurement")

    checks = models.ManyToManyField("QualityCheck", through="BrewQualityCheck")

    # sample = GenericRelation("Sample")

    def __str__(self):

        return f"{self.batch.nr} - {self.batch.beer}"

    def list_recipes(self):

        """ List all recipes possible for this brew """

        return self.batch.beer.recipes

    def list_materials(self):

        return self.brewmaterial_set.all()

    def has_transfer(self):

        return self.list_transfers().exists()

    def list_transfers(self):

        return self.tank.all()

    def list_phases(self):

        return self.phase.all()

    def list_measurements(self):

        """Return list of all related measurments."""

        return self.measurement.all()

    def list_qualitychecks(self):

        """ Return a list of all qualitychecks for the brew."""

        return self.brewqualitycheck_set.all()

    def add_phase(self, metaphase):

        """ Add phase of the metpahase given """

        self.phase.create(metaphase=metaphase, order=self.phase.count())

    def get_delay(self, phase):

        """Return delay specified on the brewhouse for given phase,
        if any."""

        if self.brewhouse.list_delays().filter(
                metaphase__name=phase.metaphase).exists():
            return self.brewhouse.list_delays().filter(
                metaphase__name=phase.metaphase).first().delay

        return Duration("0m")

    def get_total_duration(self):

        """ Return total duration of the brew """

        if not self.list_phases().exists():
            return Duration(settings.DEFAULT_BREW_TIME)

        total = Duration("0m")

        for phase in self.list_phases():

            total += phase.get_duration()
            total += self.get_delay(phase)

        return total

    @property
    def volume_projected(self):

        """ Check quality checks for final volume """

        if self.list_qualitychecks().filter(
                qc__milestone="ninkasi.brew.end").exists():
            return self.list_qualitychecks().filter(
                qc__milestone="ninkasi.brew.end").first().projected

        return 0

    @property
    def volume(self):

        """The brew volume is the volume of the last measurement
        taken.

        TODO: how to make volume configurable?
        """

        if self.list_measurements().filter(quantity__name="Volume").exists():
            return self.list_measurements().filter(
                quantity__name="Volume"
            ).last().value

        return self.volume_projected

    def import_phases(self, recipe_id):

        """Import all phases from the brew recipe, that is in fact the
        recipe of the beer for this batch.

        """

        self.list_phases().delete()

        recipe = self.batch.beer.get_recipe(recipe_id)

        for phase in recipe.list_phases():

            if phase.get_metaphase().parents.filter(model='brew').exists():

                phase.copy(self)

                # Also create quality checks
                #
                for check in phase.get_metaphase().list_qualitychecks():

                    kwargs = {'qc': check}

                    if check.constant:
                        value = check.constant
                    else:
                        value = recipe.get_milestone_value(check.milestone,
                                                           check.quantity)

                    if value:
                        kwargs['projected'] = value

                    if check.margin:
                        kwargs['margin'] = check.margin

                    self.brewqualitycheck_set.create(**kwargs)

    class Meta:

        ordering = ["batch__nr", "date"]
        verbose_name_plural = _("Brews")


class BrewMaterial(ParentedMaterial):

    """ M2M definition for a brew to materials. """

    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)


class BrewQualityCheck(models.Model):

    """ Define measurements to take during this phase """

    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
    qc = models.ForeignKey("QualityCheck", on_delete=models.CASCADE)
    projected = models.FloatField(blank=True, null=True)
    margin = models.FloatField(default=0)
    time = models.DateTimeField(blank=True, null=True)
    actual = models.FloatField(blank=True, null=True)
    notes = models.TextField(_("Notes"), null=True, blank=True)

    def __str__(self):

        """ Return readable quality check """

        return f"{ self.qc }"

    def is_ok(self):

        """ See whether the values are ok."""

        if not self.projected and self.actual:
            return False

        return (self.actual <= self.projected + self.margin and
                self.actual >= self.projected - self.margin)
