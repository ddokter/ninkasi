from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .tank import Tank


class Transfer(models.Model):

    """ Represent racking from one tank to the other. May be attached to
    brew or batch. """

    parent = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    date = models.DateTimeField(_("Date (actual)"))
    end_date = models.DateTimeField(_("Date to"), blank=True, null=True,
                                    editable=False)
    volume = models.SmallIntegerField(_("Volume"), blank=True, null=True)

    def __str__(self):

        return f"{ self.tank } { self.formatted_date } - { self.end_date }"

    @property
    def formatted_date(self):

        return self.date.strftime("%d-%m-%Y %H:%M")

    class Meta:

        ordering = ["date"]
