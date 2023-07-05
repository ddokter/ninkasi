from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from .tank import Tank
from .asset import Asset
from .unit import Unit
from .step import Step


class Batch(models.Model):

    """ One production for a given recipe. """

    nr = models.CharField(_("Nr"), max_length=100, unique=True)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    asset = models.ManyToManyField(Asset, through="BatchAsset")
    # tank = models.ManyToManyField(Tank, through="BatchTank")
    step = models.ManyToManyField(Step)  #, through="RecipeStep")    
    sample = GenericRelation("Sample")
    
    @property
    def volume(self):

        return sum([brew.volume for brew in self.list_brews()])
    
    def __str__(self):

        return f"{self.recipe.name} - #{self.nr}"

    def list_brews(self):

        return self.brew_set.all()

    def list_assets(self):

        return self.batchasset_set.all()

    class Meta:

        app_label = "ninkasi"
        ordering = ["nr"]
        verbose_name_plural = _("Batches")


class BatchTank(models.Model):

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    date_from = models.DateTimeField(_("Date from"))
    date_to = models.DateTimeField(_("Date to"))


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

        return "%s %s" % (self.asset, self.amount)
