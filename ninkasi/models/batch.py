""" Hold batch model """

from datetime import timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .tank import Tank
from .material import Material, ParentedMaterial
from .step import BatchStep


class Batch(models.Model):

    """A batch is a volume of beer that can be treated as a separate
    unit. This boils down to a volume that is brewed in one or more
    brews, fermented and packaged in one or more ways.

    The concept of a batch is mainly there to keep track of used
    resources, with their own batch numbers, but it also provides a
    focal point for measurements, like specific gravity, Ph,
    durations, etc.

    A batch goes through the following phases: brewing, fermentation,
    maturation, packaging, although the system allows for defining
    more phases.

    A batch may be split during the process over containers, or even
    blended. A blend however, effectively means that a batch cannot be
    tracked on itself anymore. The 'blend' is registered and serves as
    a new batch.

    TODO: arrange this!

    """

    nr = models.CharField(_("Nr"), max_length=100, unique=True)
    beer = models.ForeignKey("Beer", on_delete=models.CASCADE)
    material = models.ManyToManyField(Material, through="BatchMaterial")
    tank = models.ManyToManyField(Tank, through="BatchContainer")

    # tank = GenericRelation("Transfer")
    #step = GenericRelation(BatchStep)
    sample = GenericRelation("Sample")

    @property
    def volume_projected(self):

        """Total batch volume, i.e. sum of brew volumes """

        return sum([brew.volume for brew in self.list_brews()])

    def __str__(self):

        return f"{self.beer.name} - #{self.nr}"

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

    def list_phases(self):

        return self.batchphase_set.all()

    def list_materials(self):

        """ List all materials, also of sub brews """

        batch_materials = self.batchmaterial_set.all()

        for brew in self.list_brews():
            batch_materials = batch_materials.union(brew.list_materials())

        return batch_materials

    def list_tanks(self):

        return self.tank.all()

    def list_samples(self):

        """ samples may be taken from a batch. List them. """

        return self.sample_set.all()

    @property
    def start_date(self):

        """ The start date is inferred from the first brew """

        if self.list_brews().exists():

            return self.list_brews().first().date

        return None

    @property
    def end_date_projected(self):

        """ The end date according to the start date plus the number
        of days specified in the recipe """

        if self.start_date:

            return self.start_date + timedelta(
                days=self.beer.get_processing_time())

        return None

    @property
    def end_date(self):

        """ End date calculated from start date and steps """

        if self.start_date:

            return self.start_date + timedelta(
                days=self.get_total_duration())

        return None

    def get_total_duration(self, unit='day'):

        """ TODO: use days or no """

        return (sum(phase.get_duration() for phase in self.list_phases()) /
                (60 * 24))

    class Meta:

        app_label = "ninkasi"
        ordering = ["nr"]
        verbose_name_plural = _("Batches")


class BatchMaterial(ParentedMaterial):

    """Materials can be related to a batch given an amount of used
    products. This is useful to, for instance, specify the amount of
    bottles or kegs used to package the batch."""

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)


class BatchContainer(models.Model):

    """Where is the batch contained? This may be split over more than
    one container, or even blended over batches. However, a container
    cannot contain more that it's volume.

    """

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    volume = models.FloatField()  # validators=(check_tank_volume))

    #def check_tank_volume(self, value):

    #if value > self.tank.volume:
    #        raise ValidationError(_("Volume is bigger than tank volume"),
    #                              code="invalid",
    #                              params={"value": value}
    #                            )

    # TODO: make validator for checking on whether the tank is already
    # filled on these dates.

