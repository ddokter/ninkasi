from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from ninkasi.api import Style as BaseStyle
from .fields import IntRangeField


class Style(models.Model, BaseStyle):

    """The (beer) style defines the ranges in terms of color, gravity,
    bitternes, etc. and provides a description of the style. Lists of
    beer styles are provided by several sources, for example the BJCP,
    so normally these are imported. Check Ninkasi plugin apps.

    """

    name = models.CharField(_("Name"), null=True, blank=True, max_length=100)
    description = models.TextField()
    color = IntRangeField(_("Color"), max_length=10)
    source = models.CharField(_("Source"), max_length=50)

    def __str__(self):

        return self.name

    def get_color_display(self):

        """ Get display value for color range """

        lhv, rhv = self._meta.get_field('color').get_parts()

        return f"[ { lhv } .. {rhv } ] EBC"

    @property
    def urn(self):

        return f"urn:django:{ self.id }"

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
