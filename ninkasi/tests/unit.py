from django.test import TestCase
from ninkasi.models.unit import Unit, Conversion


class TestUnit(TestCase):

    """ Unit test for ninkasi.Unit. Duh. """

    def setUp(self):

        self.liter = Unit.objects.create(name="Liter", abbreviation="L")
        self.ml = Unit.objects.create(name="milliliter", abbreviation="ml")
        self.cl = Unit.objects.create(name="milliliter", abbreviation="ml")

        Conversion.objects.create(from_unit=self.liter, to_unit=self.ml,
                                  factor=0.001)

        self.liter.conversion_set.create(to_unit=self.cl, factor=0.01)

    def test_convert(self):

        """ Convert unit into another unit """

        self.assertEquals(self.liter.convert(1000, self.ml), 1.0)
        self.assertEquals(self.liter.convert(1000, self.cl), 10.0)

        self.assertEquals(self.ml.convert(1000, "Liter"), 1.0)
