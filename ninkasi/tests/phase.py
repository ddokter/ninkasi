from datetime import date, datetime
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from ninkasi.models.phase import Phase
from ninkasi.models.step import Step, MashStep
from ninkasi.models.recipe import Recipe
from ninkasi.models.fields import Duration
from ninkasi.models.batch import Batch
from ninkasi.models.brew import Brew
from ninkasi.models.brewhouse import Brewhouse
from ninkasi.models.metaphase import MetaPhase
from ninkasi.models.beer import Beer
from ninkasi.models.task import EventScheduledTask


class TestPhase(TestCase):

    """ Unit test for ninkasi.Phase """

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

        parent = Recipe.objects.create(name="testbrew0", volume=500)

        self.phase = Phase.objects.create(parent=parent,
                                          order=0, metaphase="mash")

    def test_copy(self):

        parent = Recipe.objects.create(name="testbrew1", volume=500)

        new_phase = self.phase.copy(parent)

        self.assertEquals(new_phase.order, self.phase.order)
        self.assertEquals(len(new_phase.list_steps()),
                          len(self.phase.list_steps()))

        # now let's add some steps
        #
        step0 = Step.objects.create(phase=self.phase, temperature=100,
                                    duration=Duration("60m"))

        step1 = MashStep.objects.create(phase=self.phase, temperature=10,
                                        duration=Duration("10d"))

        new_phase = self.phase.copy(parent)

        self.assertEquals(len(new_phase.list_steps()),
                          len(self.phase.list_steps()))

        self.assertEquals(len(new_phase.list_steps()), 2)

        step0_cp = new_phase.step_set.all()[0].get_real()
        step1_cp = new_phase.step_set.all()[1].get_real()

        self.assertEquals(step0.__class__, step0_cp.__class__)
        self.assertEquals(step1.__class__, step1_cp.__class__)

        self.assertEquals(step0.temperature, step0_cp.temperature)
        self.assertEquals(step1.duration, step1_cp.duration)

    def test_equals(self):

        parent = Recipe.objects.create(name="testbrew1", volume=500)

        new_phase = self.phase.copy(parent)

        self.assertTrue(new_phase == self.phase)

        # now let's add some steps
        #
        Step.objects.create(phase=self.phase, temperature=100,
                            duration=Duration("60m"))

        MashStep.objects.create(phase=self.phase, temperature=10,
                                duration=Duration("10d"))

        new_phase = self.phase.copy(parent)

        self.assertTrue(new_phase == self.phase)

        new_phase.metaphase = "foobar"

        self.assertFalse(new_phase == self.phase)

    def test_generate_tasks(self):

        """ See whether we can generate tasks associated with this phase """

        now = datetime.now()

        beer = Beer.objects.create(
            name="Keuls",
            description="Dikke vette keuls",
            style="style:django:1"
        )

        batch = Batch.objects.create(
            nr="666",
            beer=beer,
            volume_projected=500,
            date=date.today(),
            date_mode=0
        )

        brewhouse = Brewhouse.objects.create(
            warmup=1,
            next_brew_delay="8h",
            filter_loss=20,
            spent_grain_loss=1,
            whirlpool_loss=10,
            volume=500
        )

        brew = Brew.objects.create(
            batch=batch,
            brewhouse=brewhouse,
            date=now,
            volume_projected=500
        )

        phase0 = batch.phase.create(
            parent=batch,
            order=0,
            metaphase="fermentation")

        EventScheduledTask.objects.create(
            name="Doe dingen",
            description="Wat ik zeg",
            precision="5m",
            event="ninkasi.Fermentation.start"
        )

        phase0.generate_tasks(parent=batch)

        self.assertEquals(phase0.tasks.count(), 1)
