from django.db import models
from django.utils.translation import gettext_lazy as _


class Asset(models.Model):

    """ Anything needed for a batch. Can be an ingredient, but also bottles
    or labels """

    name = models.CharField(_("Name"), max_length=100)
    category = models.ManyToManyField("Category", blank=True)
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)

    def __str__(self):

        return self.name

    @property
    def categories(self):

        return [str(cat) for cat in self.category.all()]

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]
