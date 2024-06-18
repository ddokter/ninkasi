from django.db import models
from django.utils.translation import gettext_lazy as _


class Unit(models.Model):

    """Represent units in the system, for weight, volume, etc. The
    unit is related to a quantity. Units may hold a table of
    conversions to other units, including those related through metric
    conversions.

    """

    name = models.CharField(_("Name"), max_length=100, unique=True)
    abbreviation = models.CharField(_("Abbreviation"), max_length=50,
                                    null=True, blank=True)
    subs = models.ManyToManyField("Unit", through="Conversion")

    def __str__(self):

        return self.abbreviation or self.name

    def convert(self, amount, unit):

        """Convert unit to other, must be related through
        conversions."""

        if isinstance(unit, str):
            unit = Unit.objects.get(name=unit)

        if unit == self:

            return amount

        if self.conversion_set.filter(to_unit=unit).exists():
            return self.conversion_set.get(to_unit=unit).factor * amount

        return unit.conversion_set.get(to_unit=self).factor * amount

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Units")


class Conversion(models.Model):

    """Represent a conversion from one unit to another."""

    from_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    to_unit = models.ForeignKey(Unit, related_name="to_unit",
                                on_delete=models.CASCADE)
    factor = models.FloatField()

    fk_name = "from_unit"

    def __str__(self):

        return f"{ self.from_unit } * { self.factor } = { self.to_unit }"
