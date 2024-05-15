""" Hold batch model """

from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .tank import Tank
from .material import Material, ParentedMaterial
from .fields import Duration


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

    The batch is used as a vehicle for planning. That means that the
    batch has a projected volume and a projected end date.

    """

    nr = models.CharField(_("Nr"), max_length=100, unique=True)
    beer = models.ForeignKey("Beer", on_delete=models.CASCADE)
    volume_projected = models.FloatField(_("Planned volume"))
    delivery_date = models.DateField()

    material = models.ManyToManyField(Material, through="BatchMaterial")
    tank = models.ManyToManyField(Tank, through="BatchContainer")

    phase = GenericRelation("Phase")
    sample = GenericRelation("Sample")

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

        """ A batch may consist of several brews """

        return self.brew_set.all()

    def list_phases(self):

        """ Get all phases defined for this batch """

        return self.phase.all()

    def list_materials(self):

        """ List all materials, also of sub brews """

        batch_materials = self.batchmaterial_set.all()

        for brew in self.list_brews():
            batch_materials = batch_materials.union(brew.list_materials())

        return batch_materials

    def list_tanks(self):

        """ List all tank transfers for the batch """

        return self.tank.all()

    def list_samples(self):

        """ samples may be taken from a batch. List them. """

        return self.sample_set.all()

    @property
    def start_date(self):

        """ The start date calculated from the delivery_date. Time needed
        will be subtracted to determine start date. The start date
        is projected. If a brew is added, it may reset the start date."""

        if self.list_brews().exists():

            return self.list_brews().first().date.date()

        return self.delivery_date - timedelta(
            days=self.get_processing_time().days)

    def get_total_duration(self):

        """ Get duration based on phases """

        return sum(phase.get_duration() for phase in self.list_phases())

    def get_processing_time(self):

        """ Get the time needed to process this batch.
        """

        try:
            return self.get_recipe().get_total_duration()
        except AttributeError:
            return Duration(settings.DEFAULT_PROCESSING_TIME)

    def import_phases(self, recipe_id):

        """Import all phases from the batch recipe, that is in fact
        the recipe of the beer for this batch. In the future, this
        could be a choice of many.
        """

        for phase in self.beer.get_recipe(recipe_id).list_phases():

            if 'batch' in phase.get_metaphase().parents:

                phase.copy(self)

    def get_recipe(self):

        """ Get the recipe set for this batch """

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
