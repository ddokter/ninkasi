""" Register event handlers for Django's signals """

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .batch import BatchContainer
from .step import Step, MashStep
from .brew import Brew
from .task import MilestoneScheduledTask
from .phase import Phase


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


@receiver(post_save, sender=BatchContainer)
def batchcontainer_post_save(sender, instance, **kwargs):

    """ Check on fill and empty date and generate tasks accordingly """

    if instance.from_date:

        for milestone in MilestoneScheduledTask.objects.filter(milestone=1):

            milestone.generate_tasks(
                parent=instance.batch,
                date=instance.from_date.date(),
                time=instance.from_date.time(),
                name=f"{ milestone.name } { instance.tank }"
            )

    if instance.to_date:

        for milestone in MilestoneScheduledTask.objects.filter(milestone=0):

            milestone.generate_tasks(
                parent=instance.batch,
                date=instance.to_date.date(),
                time=instance.to_date.time(),
                name=f"{ milestone.name } { instance.tank }"
            )


@receiver(post_save, sender=Phase)
def phase_post_save(sender, instance, **kwargs):

    """Whenever a phase changes, recreate any tasks associated with
    it to make sure timings are correct

    """

    instance.generate_tasks()
