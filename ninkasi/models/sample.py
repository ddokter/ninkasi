from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from .step import Step


class Sample(models.Model):

    """Samples are taken from specific stages in the brew process and
    may be related to a batch or a brew. A sample may (and should)
    express a number of measurements.

    """

    parent = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    date = models.DateTimeField(_("Time"))
    # step = models.ForeignKey(Step, on_delete=models.CASCADE)
    notes = models.CharField(_("Notes"), max_length=200, null=True,
                             blank=True)

    def list_measurements(self):

        """ List all measurements that are taken from this sample """

        return self.measurement_set.all()

    def __str__(self):

        return f"{self.parent} {self.step}"

    class Meta:

        app_label = "ninkasi"
        ordering = ['date']
