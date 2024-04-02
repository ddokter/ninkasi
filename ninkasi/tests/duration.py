from django.test import TestCase
from ninkasi.models.fields import Duration


class TestDuration(TestCase):

    """ Unit test for Duration """

    def setUp(self):

        self.duration = Duration("10m")

    def test_add(self):

        self.duration += Duration("1h")

        self.assertEquals(self.duration.amount, 70)

        d0 = Duration("10m")
        d2 = Duration("3600s")
        d1 = Duration("1d")
        d3 = Duration("2h")

        d4 = sum([d0, d1, d2, d3])

        self.assertEquals(str(d4), "1630.0m")
