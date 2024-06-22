""" Unit test for ninkasi.Batch """

from datetime import date, datetime, timedelta
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from ninkasi.models.phase import Phase
from ninkasi.models.batch import Batch
from ninkasi.models.beer import Beer
from ninkasi.models.metaphase import MetaPhase
from ninkasi.models.brew import Brew
from ninkasi.models.brewhouse import Brewhouse


class TestBatch(TestCase):

    """ Unit test for ninkasi.Batch """

    def setUp(self):

        default_step = ContentType.objects.filter(
            app_label="ninkasi",
            model__icontains="step").first()

        mash = MetaPhase.objects.create(
            name="mash",
            default_step=default_step)
        ferm = MetaPhase.objects.create(
            name="fermentation",
            default_step=default_step)
        matr = MetaPhase.objects.create(
            name="maturation",
            default_step=default_step)

        beer = Beer.objects.create(
            name="Keuls",
            description="Dikke vette keuls",
            style="style:django:1"
        )

        self.brewhouse = Brewhouse.objects.create(
            warmup=1,
            next_brew_delay="8h",
            filter_loss=20,
            spent_grain_loss=1,
            whirlpool_loss=10,
            volume=500
        )

        self.batch = Batch.objects.create(
            nr="666",
            beer=beer,
            volume_projected=500,
            date=date.today(),
            date_mode=0
        )

    def test_get_phase_start(self):

        """ Check on start dates of batch related phases """

        now = datetime.now()

        brew = Brew.objects.create(
            batch=self.batch,
            brewhouse=self.brewhouse,
            date=now,
            volume_projected=500
        )

        phase0 = self.batch.phase.create(
            order=0,
            metaphase="fermentation")

        phase0.step_set.create(
            name="step0",
            duration="30m"
        )

        phase1 = self.batch.phase.create(
            order=1,
            metaphase="maturation")

        start = self.batch.get_phase_start(phase1.id)

        self.assertEquals((now + timedelta(minutes=30)).timestamp(),
                          start.timestamp())
