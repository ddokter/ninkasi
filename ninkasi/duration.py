""" All duration stuff """

import re
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Duration field regexp
#
DURATION_RE = re.compile(r"^(\-?[0-9]+\.?[0-9]*)\s*([smhd])$")

# Map duration to minutes
#
DURATION_MAP = {
    'd': 60 * 24,
    'm': 1,
    'h': 60,
    's': 1/60
}


def convert_duration(value, unit="m"):

    """Take a Duration value and convert it to the unit provided.

    """

    if isinstance(value, str):
        value = Duration(value)

    return (value.amount * DURATION_MAP[value.unit]) / DURATION_MAP[unit]


class Duration:

    """ Duration object, specifying an amount and a unit """

    def __init__(self, value):

        res = DURATION_RE.match(value)

        try:
            self.amount = float(res.group(1))
            self.unit = res.group(2)
        except AttributeError as exc:
            raise ValidationError(_("Improper format for duration")) from exc

    def __str__(self):

        return f"{self.amount:.2f}{ self.unit }"

    def convert(self, unit):

        """ Convert to the value asked """

        return convert_duration(self, unit=unit)

    @property
    def days(self):

        """ Convenience property, returning the number of days """

        return self.convert(unit="d")

    @classmethod
    def from_dates(cls, start, end):

        """ Calculate a duration from two dates """

        return Duration(f"{ (end - start).total_seconds() / 60 }m")

    def as_timedelta(self):

        """ Return the duration as timedelta object """

        return timedelta(days=self.days)

    def __len__(self):

        return len(str(self))

    def __add__(self, value):

        """ Add another duration. Convert to same unit. """

        self.amount += convert_duration(str(value), unit=self.unit)

        return self

    def __sub__(self, value):

        """ Subtract another duration. Convert to same unit. """

        self.amount -= convert_duration(str(value), unit=self.unit)

        return self

    def __radd__(self, other):

        """ Allow summation """

        if other == 0:
            return self

        return self.__add__(other)

    def __eq__(self, thing):

        if not isinstance(thing, self.__class__):
            return False

        return (self.amount == thing.amount and self.unit == thing.unit)

    def abs(self):
        """ Return abs for amount """

        return f"{abs(self.amount):.2f}{ self.unit }"
