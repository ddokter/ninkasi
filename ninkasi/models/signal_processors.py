from datetime import timedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .batch import Batch
from .transfer import Transfer
from .step import Step, MashStep
from .brew import Brew


def recalc_end_dates(batch, transfer=None):

    """Set end date to either delivery date of batch, or to date of
    next transfer. Use 'update' to prevent further signals

    """

    transfers = batch.list_transfers()

    for i, transfer in enumerate(transfers):
        try:
            Transfer.objects.filter(id=transfer.id).update(
                end_date=transfers[i + 1].date)
        except IndexError:
            Transfer.objects.filter(id=transfer.id).update(
                end_date=batch.end_date_projected)


@receiver(post_save, sender=Transfer)
def transfer_post_save(sender, instance, **kwargs):

    """ Handle Transfer post save """

    recalc_end_dates(instance.parent, transfer=instance)


@receiver(post_save, sender=Batch)
def batch_post_save(sender, instance, **kwargs):

    """ Handle signal for batch, where end date may be involved """

    # recalc_end_dates(instance)


@receiver(post_save, sender=Brew)
def brew_post_save(sender, instance, **kwargs):

    """ Set date of batch, if needed """

    if not instance.batch.list_brews().exclude(id=instance.id).filter(
            date__lt=instance.date).exists():
        instance.batch.date = instance.date
        instance.batch.save()


@receiver(pre_save, sender=Step)
def step_pre_save(sender, instance, **kwargs):

    if not instance.order:

        try:
            instance.order = instance.phase.step_set.last().order + 1
        except AttributeError:
            pass


@receiver(pre_save, sender=MashStep)
def mashstep_pre_save(sender, instance, **kwargs):
    
    step_pre_save(sender, instance, **kwargs)
