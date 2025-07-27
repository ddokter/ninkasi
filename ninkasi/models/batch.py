""" Hold batch model """

from datetime import datetime, date
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from ..ordered import OrderedContainer
from .tank import Tank
from .material import Material, ParentedMaterial
from .fields import Duration, ColorField
from ..milestones import MilestoneProviderModel
from .task import MilestoneScheduledTask
from .inventoryitem import InventoryItem


DATE_MODE_VOCAB = [(0, _("Start")), (1, _("Delivery"))]


STATUS_PLANNED = 1
STATUS_BREWING = 2
STATUS_ARCHIVED = 3


class Batch(models.Model, OrderedContainer, MilestoneProviderModel):

    """A batch is a volume of beer that can be treated as a separate
    unit. This boils down to a volume that is brewed in one or more
    brews, fermented and packaged in one or more ways.

    The concept of a batch is mainly there to keep track of used
    resources, with their own batch numbers, but it also provides a
    focal point for measurements, like specific gravity, Ph,
    durations, etc.

    A batch goes through the following phases: brewing, fermentation,
    maturation, packaging, although the system allows for defining
    more phases.

    A batch may be split during the process over containers, or even
    blended. A blend however, effectively means that a batch cannot be
    tracked on itself anymore. The 'blend' is registered and serves as
    a new batch.

    TODO: arrange this!

    The batch is used as a vehicle for planning. That means that the
    batch has a projected volume and a projected end date.

    """

    nr = models.CharField(_("Nr"), max_length=100, unique=True)
    beer = models.ForeignKey("Beer", on_delete=models.CASCADE)
    volume_projected = models.FloatField(_("Planned volume"))
    date = models.DateField()
    date_mode = models.SmallIntegerField(choices=DATE_MODE_VOCAB)

    material = models.ManyToManyField(Material, through="BatchMaterial")
    tank = models.ManyToManyField(Tank, through="BatchContainer")
    product = models.ManyToManyField("Product", through="Deliverable")

    phase = GenericRelation("Phase")
    sample = GenericRelation("Sample")
    measurement = GenericRelation("Measurement")

    color = ColorField(_("Color"), max_length=7, null=True, blank=True)

    task = GenericRelation("MilestoneTaskSub")

    def __str__(self):

        return f"{self.beer.name} - #{self.nr}"

    def __abbr__(self):

        """ Return short name """

        return f"#{self.nr:08s}"

    def get_status(self):

        """ Return status of batch """

        today = date.today()

        if today < self.start_date:
            return STATUS_PLANNED
        elif today > self.delivery_date:
            return STATUS_ARCHIVED
        else:
            return STATUS_BREWING

    @property
    def start_date_projected(self):

        """ The start date as planned. That is either the date field
        set and the mode 'start date', or the delivery date minus the
        processing time. """

        if self.date_mode == 0:

            return self.date

        return self.date - self.get_processing_time().as_timedelta()

    @property
    def start_date(self):

        """ Return the actual start date. This is the date of the first
        brew or None """

        if self.list_brews().exists():
            return self.list_brews().first().date.date()

        return self.start_date_projected

    @property
    def start_time(self):

        """ Return the start time, if set at all. """

        if self.list_brews().exists():
            return self.list_brews().first().date

        return None

    @property
    def delivery_date_projected(self):

        """ Return delivery date, either calculated or from field """

        if self.date_mode == 1:

            return self.date

        return self.date + self.get_processing_time().as_timedelta()

    @property
    def delivery_date(self):

        """ Return the actual delivery date, calulated from start_date if
        possible. """

        return self.start_date + self.get_processing_time().as_timedelta()

    @property
    def volume(self):

        """ Volume of brew total """

        return sum(brew.volume for brew in self.list_brews())

    def list_brews(self):

        """ A batch may consist of several brews """

        return self.brew_set.all()

    def list_phases(self):

        """ Get all phases defined for this batch """

        return self.phase.all()

    def list_deliverables(self):

        """ Get all products defined for this batch """

        return self.deliverable_set.all()

    def total_product_volume(self):

        return sum(product.total_volume() for product in
                   self.list_deliverables())

    def get_phase(self, _id):

        return self.phase.get(_id)

    def add_phase(self, metaphase):

        """ Add phase of the metpahase given """

        self.phase.create(metaphase=metaphase, order=self.phase.count())

    def get_phase_start(self, _id):

        """ Retrieve the time this phase starts. This is based on the
        batch start, with all phases in between added. """

        start = self.start_time

        if not isinstance(start, datetime):

            return None

        for phase in self.list_phases():

            if phase.id == _id:

                break

            start += phase.get_duration().as_timedelta()

        return start

    def list_batchmaterials(self):

        """ List all materials, also of sub brews """

        materials = []

        for material in self.batchmaterial_set.all():
            materials.append(material)

        for brew in self.list_brews():
            for material in brew.list_brewmaterials():
                materials.append(material)

        for deliverable in self.list_deliverables():
            for material in deliverable.product.list_productmaterials():

                material.batch = self
                materials.append(material)

        for material in materials:

            try:
                material.stock = InventoryItem.objects.filter(
                    material=material.material).aggregate(
                        Sum("amount"))['amount__sum']
            except AttributeError:
                pass

        return materials

    def list_tanks(self):

        """ List all tank transfers for the batch """

        return self.tank.all()

    def list_samples(self):

        """ samples may be taken from a batch. List them. """

        return self.sample_set.all()

    def get_total_duration(self):

        """ Get duration based on phases """

        if self.list_phases().exists():
            total = sum(phase.get_duration() for phase in self.list_phases())

            for brew in self.list_brews():
                total += brew.get_total_duration()
        else:
            total = Duration(settings.DEFAULT_PROCESSING_TIME)

        return total

    def get_processing_time(self):

        """ Get the time needed to process this batch.
        """

        return self.get_total_duration()

    def import_phases(self, recipe_id):

        """Import all phases from the batch recipe, that is in fact
        the recipe of the beer for this batch. In the future, this
        could be a choice of many.
        """

        self.list_phases().delete()

        for phase in self.beer.get_recipe(recipe_id).list_phases():

            if phase.get_metaphase().parents.filter(model='batch').exists():

                phase.copy(self)

    def get_recipe(self):

        """ Get the recipe set for this batch """

    def list_measurements(self):

        """ Return all related measurements """

        return self.measurement.all()

    def generate_tasks(self, **kwargs):

        """Create tasks associated with this batch, if at all
        possible.  Batch tasks are milestone based, and the start_time of
        the batch must be set to be able to determine this.

        """

        if not self.start_time:
            return False

        kwargs.update({'parent': self})

        for milestone in self.list_milestones():

            if milestone == "ninkasi.batch.start":
                date = self.start_time.date()
                time = self.start_time.time()
            elif milestone == "ninkasi.batch.end":
                date = self.delivery_date_projected
                time = None

            for task in MilestoneScheduledTask.objects.filter(
                    milestone=milestone):

                task.generate_tasks(date=date, time=time, **kwargs)

    def is_related(self):

        return self.original.exists() or self.spawned.exists()

    def get_related(self):

        return self.original.all() | self.spawned.all()

    class Meta:

        app_label = "ninkasi"
        ordering = ["date"]
        verbose_name_plural = _("Batches")


class BatchMaterial(ParentedMaterial):

    """Materials can be related to a batch given an amount of used
    products. This is useful to, for instance, specify the amount of
    bottles or kegs used to package the batch."""

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)


class BatchContainer(models.Model):

    """Where is the batch contained? This may be split over more than
    one container, or even blended over batches. However, a container
    cannot contain more that it's volume.

    """

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    volume = models.FloatField()  # validators=(check_tank_volume))

    # def check_tank_volume(self, value):

    # if value > self.tank.volume:
    #        raise ValidationError(_("Volume is bigger than tank volume"),
    #                              code="invalid",
    #                              params={"value": value}
    #                            )

    # TODO: make validator for checking on whether the tank is already
    # filled on these dates.


class Deliverable(models.Model):

    """Relate batch to product to be delivered."""

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    amount = models.SmallIntegerField()
    deadline = models.DateTimeField(null=True, blank=True)

    def total_volume(self):

        """ Return the total volume of the batchproduct """

        return self.amount * self.product.get_liter_volume()

    def __str__(self):

        return f"{self.product} * {self.amount}"


class BatchQualityCheck(models.Model):

    """ Define measurements to take during this phase """

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    qc = models.ForeignKey("QualityCheck", on_delete=models.CASCADE)
    projected = models.FloatField(blank=True, null=True)
    margin = models.FloatField(default=0)
    time = models.DateTimeField(blank=True, null=True)
    actual = models.FloatField(blank=True, null=True)
    notes = models.TextField(_("Notes"), null=True, blank=True)

    def get_parent(self):

        """ Return parent batch """

        return self.batch

    def __str__(self):

        """ Return readable quality check """

        return f"{self.qc}"

    def is_ok(self):

        """ See whether the values are ok."""

        if not self.projected and self.actual:
            return False

        return (self.actual <= self.projected + self.margin and
                self.actual >= self.projected - self.margin)


class Batch2Batch(models.Model):

    """ Relate batches """

    MERGE = 0
    SPLIT = 1

    original = models.ForeignKey(Batch,
                                 related_name='original',
                                 on_delete=models.CASCADE)
    spawned = models.ForeignKey(Batch,
                                related_name='spawned',
                                on_delete=models.CASCADE)
    relation = models.SmallIntegerField(choices=[(MERGE, MERGE),
                                                 (SPLIT, SPLIT)])
    date = models.DateTimeField(default=timezone.now)
