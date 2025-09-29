from django.db import models
from django.utils.translation import gettext_lazy as _


COLOR_HELP = _("Specify color in EBC")
BITTERNESS_HELP = _("Specify as IBU")
OG_HELP = _("Gravity in SG, e.g. 1.048")


class Beer(models.Model):

    """A beer is defined by it's name, style, description and parameters
    that define it: color, bitterness, og and abv.

    A beer can be further linked to one or more recipes. This may
    sound counterintuitive, but imagine a strong beer that can be
    brewed on a given brewhouse in one go, but on another, with
    different geometry, only with a double mash. Another example is a
    sour, that may be brewed using kettle souring, or alternatively
    using a hybrid yeast, to produce the same beer.

    """

    name = models.CharField(_("Name"), max_length=100)
    style = models.ForeignKey("Style", on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    color = models.IntegerField(help_text=COLOR_HELP)
    bitterness = models.IntegerField(help_text=BITTERNESS_HELP)
    og = models.FloatField(help_text=OG_HELP)
    abv = models.FloatField()

    def __str__(self):

        return self.name

    def list_batches(self):

        """ All batches for this beer """

        return self.batch_set.all()

    def list_recipes(self):

        """ List all related recipes """

        return self.recipe_set.all()

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
