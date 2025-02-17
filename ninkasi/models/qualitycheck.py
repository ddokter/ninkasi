"""Qualitycheck model and utils"""

from django.utils.translation import gettext_lazy as _
from django.db import models
from .fields import DurationField, MilestoneField
from ..milestones import MilestoneRegistry


OFFSET_HELP = _("Offset to milestone. Use negative amounts to "
                "specify time before")

CONSTANT_HELP = _("If the quantity can be specified as constant across"
                  "recipes, define the projected value here.")


def milestone_vocab():

    """ Provide vocabulary for milestones """

    return [(evt, evt) for evt in MilestoneRegistry.list_milestones()]


class QualityCheck(models.Model):

    """Define quantities that should be measured at the given
    milestone. Ninkasi does not make any assumptions on what checks to
    do, the brewery itself should decide what measurements are
    defining the quality of their beer.

    """

    quantity = models.ForeignKey("Quantity", on_delete=models.CASCADE)
    milestone = MilestoneField(max_length=100, choices=milestone_vocab)
    offset = DurationField(default="0m", help_text=OFFSET_HELP)
    constant = models.FloatField(null=True, blank=True,
                                 help_text=CONSTANT_HELP)
    margin = models.FloatField(null=True, blank=True,
                               help_text=_("Allow margin"))

    def __str__(self):

        """ Return readable quality check """

        _str = f"{ self.quantity } @ { self.milestone }"

        if self.offset.amount:

            _str += f" { self.offset.get_sign() } { self.offset }"

        return _str
