from datetime import timedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .batch import Transfer, Batch


def recalc_end_dates(batch, transfer=None):

    transfers = batch.transfer_set.all()

    for i, transfer in enumerate(transfers):
        try:
            Transfer.objects.filter(id=transfer.id).update(
                end_date=transfers[i + 1].date)
        except IndexError:
            Transfer.objects.filter(id=transfer.id).update(
                end_date=batch.deliverydate)


@receiver(post_save, sender=Transfer)
def transfer_post_save(sender, instance, **kwargs):

    """ Set end date to either deliverydate of batch, or to
    date of next transfer """

    recalc_end_dates(instance.batch, transfer=instance)


@receiver(pre_save, sender=Batch)
def batch_pre_save(sender, instance, **kwargs):

    if not instance.deliverydate:
        now = timezone.now()

        instance.deliverydate = (
            now + timedelta(days=instance.recipe.get_total_duration()))


@receiver(post_save, sender=Batch)
def batch_post_save(sender, instance, **kwargs):

    """ Set end date to either deliverydate of batch, or to
    date of next transfer """

    recalc_end_dates(instance)
