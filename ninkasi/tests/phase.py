from django.test import TestCase
from ninkasi.models.phase import Phase
from ninkasi.models.step import Step, MashStep
from ninkasi.models.recipe import Recipe
from ninkasi.models.fields import Duration


class TestPhase(TestCase):

    """ Unit test for ninkasi.Phase """

    def setUp(self):

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
