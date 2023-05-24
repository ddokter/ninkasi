from django.db import models
from django.utils.translation import gettext_lazy as _


TTYPE_VOCAB = [
    (0, "Fermentation"),
    (1, "BBT"),
    (2, "Lagering")
]


class Tank(models.Model):

    """Base class for all tanks. For now we use this as the only
    model, maybe later switching to polymorphism.
    """

    name = models.CharField(_("Name"), null=True, blank=True, max_length=100)
    volume = models.SmallIntegerField(_("Volume"))
    ttype = models.SmallIntegerField(_("Type"),
                                     default=0,
                                     choices=TTYPE_VOCAB,
                                     )


    def __str__(self):

        return self.name

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Tanks")


class BBT(Tank):

    """Bright beer tank

    """

    class Meta:

        app_label = "ninkasi"
        verbose_name_plural = _("BBTs")


class CCT(Tank):

    """ Conical-cylindrical tank """

    class Meta:

        app_label = "ninkasi"
        verbose_name_plural = _("CCTs")


class LagerTank(Tank):

    """ Lager tank """

    class Meta:

        app_label = "ninkasi"
        verbose_name_plural = _("Lager tanks")
