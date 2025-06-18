"""Brew model and related models for m2m relations."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from ..ordered import OrderedContainer
from .material import Material, ParentedMaterial
from ..milestones import MilestoneProviderModel
from ..duration import Duration
from .task import MilestoneScheduledTask


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

    def get_parent(self):

        return self.batch

    def __abbr__(self):

        """ Return the short name of this brew """

        return f"#{self.batch.nr} brew nr.{self.order_in_batch}"

    def __str__(self):

        return (f"#{self.batch.nr} brew nr.{self.order_in_batch}"
                f"- {self.batch.beer}")

    @property
    def order_in_batch(self):

        """ return the order in the batch, starting from 1 """

        return [id for id in self.batch.list_brews().values_list(
            "id", flat=True).order_by("date")].index(self.id) + 1

    def list_recipes(self):

        """ List all recipes possible for this brew """

        return self.batch.beer.recipes

    def list_brewmaterials(self):

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

        """Check quality checks projected volume. If none exists,
        take the brewhouse volume.

        """

        if self.list_qualitychecks().filter(
                actual__isnull=False,
                qc__milestone="ninkasi.brew.end",
                qc__quantity__name="Volume").exists():
            return self.list_qualitychecks().filter(
                actual__isnull=False,
                qc__milestone="ninkasi.brew.end",
                qc__quantity__name="Volume"
            ).first().projected or 0

        return self.brewhouse.volume

    @property
    def volume(self):

        """The brew volume is the volume of the last measurement
        taken, if there is one. Otherwise 0 will be returned.
        """

        if self.list_qualitychecks().filter(
                actual__isnull=False,
                qc__quantity__name="Volume").exists():
            return self.list_qualitychecks().filter(
                actual__isnull=False,
                qc__quantity__name="Volume"
            ).last().actual

        return 0

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

    def generate_tasks(self, **kwargs):

        """Create tasks associated with this brew, if at all possible.

        """

        if not self.date:
            return False

        kwargs.update({'parent': self, 'date': self.date.date(),
                       'time': self.date.time()})

        for milestone in self.list_milestones():

            for task in MilestoneScheduledTask.objects.filter(
                    milestone=milestone):

                task.generate_tasks(**kwargs)

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

    def get_parent(self):

        """ Return parent brew """

        return self.brew

    def __str__(self):

        """ Return readable quality check """

        return f"{self.qc}"

    def is_ok(self):

        """ See whether the values are ok."""

        if not self.projected and self.actual:
            return False

        return (self.actual <= self.projected + self.margin and
                self.actual >= self.projected - self.margin)
