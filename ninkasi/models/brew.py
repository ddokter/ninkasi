from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from .step import BatchStep
from .material import Material, ParentedMaterial


class Brew(models.Model):

    """One brew. This boils down to one full brewing cycle on the
    brewhouse. One or more brews make up a batch.

    """

    batch = models.ForeignKey("Batch", on_delete=models.CASCADE)
    brewhouse = models.ForeignKey("Brewhouse", on_delete=models.CASCADE)
    date = models.DateTimeField(_("Time"))
    material = models.ManyToManyField(Material, through="BrewMaterial")
    volume_projected = models.FloatField()

    step = GenericRelation(BatchStep)
    tank = GenericRelation("Transfer")
    sample = GenericRelation("Sample")

    def __str__(self):

        return f"{self.batch.nr} - {self.batch.beer}"

    def list_materials(self):

        return self.brewmaterial_set.all()

    def list_steps(self):

        return self.step.all()

    def has_transfer(self):

        return self.list_transfers().exists()

    def list_transfers(self):

        return self.tank.all()

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

        ordering = ["batch__nr", "date"]
        verbose_name_plural = _("Brews")


class BrewMaterial(ParentedMaterial):

    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
