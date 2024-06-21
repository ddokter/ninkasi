from django.utils.translation import gettext_lazy as _
from django.db import models
from .fields import DurationField, MilestoneField
from ..milestones import MilestoneRegistry


OFFSET_HELP_TEXT = _("Offset to milestone. Use negative amounts to "
                     "specify before")


def milestone_vocab():

    """ Provide vocabulary for milestones """

    return [(evt, evt) for evt in MilestoneRegistry.list_milestones()]


class QualityCheck(models.Model):

    """ Define measurements to take during this phase """

    quantity = models.ForeignKey("Quantity", on_delete=models.CASCADE)
    milestone = MilestoneField(max_length=100, choices=milestone_vocab)
    offset = DurationField(default="0m", help_text=OFFSET_HELP_TEXT)

    def __str__(self):

        """ Return readable quality check """

        return f"{ self.quantity } @ { self.milestone } { self.offset }"
