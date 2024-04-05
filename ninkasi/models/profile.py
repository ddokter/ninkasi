from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):

    """Base class for profiles, such as fermentation, mash,
    maturation, etc.

    """

    name = models.CharField(_("Name"), max_length=100, unique=True)

    def __str__(self):

        return self.name

    def get_duration(self, unit='h'):

        """Return the total duration of this profile in the unit
        given.  Standard is 'H'. Must be one of: second (s), minute (m),
        hour (h), day (d).

        """

    def list_steps(self):

        """ List steps, ordered """

    class Meta:
        app_label = "ninkasi"
        abstract = True
