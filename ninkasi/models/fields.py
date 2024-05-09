""" Ninkasi specific fields """

import re
from datetime import timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from ninkasi.resource import ResourceRegistry


RANGE_FIELD_SEP = ","
URN_SEP = ":"

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

    def to_timedelta(self):

        return timedelta(days=self.days)

    def __len__(self):

        return len(str(self))

    def __add__(self, value):

        """ Add another duration. Convert to same unit. """

        self.amount += convert_duration(str(value), unit=self.unit)

        return self

    def __radd__(self, other):

        """ Allow summation """

        if other == 0:
            return self

        return self.__add__(other)

    def __eq__(self, thing):

        if not thing:
            return False

        return (self.amount == thing.amount and self.unit == thing.unit)


def validate_urn(value):

    """Validate the value as URN, according to RFC2141 (note: there
    is a newer spec, but we don't need it.

    """

    try:
        (prot, nid, nss) = value.split(URN_SEP)
        assert prot == "urn"
    except (ValueError, AssertionError) as exc:
        raise ValidationError(
            _("Enter a valid urn (RFC2141)"), code="invalid",
            params={"value": value}
        ) from exc


def validate_urn_list(value):

    """ Check on the list of URN values and check 'm all """

    for urn in value.split():

        validate_urn(urn)


def validate_range(value, _type=int):

    """ Check whether the value is a comma separated tuple of floats """

    try:
        lhv, rhv = value.split(RANGE_FIELD_SEP)
        _type(lhv)
        _type(rhv)
    except ValueError as exc:
        raise ValidationError(
            _(f"Enter a valid tuple of { _type }s."), code="invalid",
            params={"value": value}
        ) from exc


def validate_int_range(value):

    """ Check whether the given value is a tuple of ints """

    return validate_range(value)


def validate_float_range(value):

    """ Check whether the given value is a tuple of floats """

    return validate_range(value, _type=float)


def validate_duration(value):

    """ Check whether the value is a '' separated tuple of float/str """

    if not value.amount and value.unit:
        raise ValidationError(
            _("Enter a valid tuple of float/str."), code="invalid",
            params={"value": value}
        )


class DurationField(models.CharField):

    """ Store tuple of float, str for duration and unit. Unit
    should be one of s, m, h, d. """

    default_validators = [validate_duration]

    def get_parts(self, value):

        """ Return the two parts of the duration, i.e. amount and unit """

        res = DURATION_RE.match(value)

        return (res.group(1), res.group(2))

    def get_duration(self, value, unit="m"):

        """ Get the duration in the given unit """

        return convert_duration(value, unit=unit)

    def to_python(self, value):

        """ Return Duration object, but gracefully """

        if isinstance(value, Duration):
            return value

        if value is None:
            return value

        return Duration(value)

    def from_db_value(self, value, *args):

        """ Convert from DB value into python value stored on the model """

        if value is None or value == '':
            return value

        return Duration(value)

    def get_prep_value(self, value):

        """ Prepare for DB, cast to str """

        return str(value)


class BaseRangeField(models.CharField):

    """ Base class """

    def get_parts(self, value):

        """ Split value into parts """

        return value.split(RANGE_FIELD_SEP)


class IntRangeField(models.CharField):

    """ Store range of min,max integers """

    default_validators = [validate_int_range]


class FloatRangeField(models.CharField):

    """ Store range of min,max floats """

    default_validators = [validate_float_range]


class URNMixin:

    registry = None

    def __init__(self, *args, **kwargs):

        self.registry = kwargs.get('registry')

        kwargs.pop('registry')

        super().__init__(*args, **kwargs)

    def get_id(self, value):

        """ Return the resource ID within the namespace """

        return value.split(URN_SEP)[2]

    def get_ns(self, value):

        """ Return the namespace """

        return value.split(URN_SEP)[1]


class URNField(URNMixin, models.CharField):

    """Resources, like recipe's, may come from many different
    sources.  Ninkasi uses a URN field to specify the provider and the
    unique ID.

    """

    default_validators = [validate_urn]

    def __to_python(self, value):

        """Return Model object if possible.  TODO: this method should
        be very conservative. So check for the correct python result,
        as it may already have been called.

        """

        if isinstance(value, models.Model) or value is None:
            return value

        nid = self.get_ns(value)
        _id = self.get_id(value)

        res = ResourceRegistry.get_resource(self.registry, nid)

        return res.get(_id)

    def from_db_value(self, value, *args):

        """ Convert from DB value into python value stored on the model.
        This makes sure the model.< fieldname > value is the actual
        resource.
        """

        return self.__to_python(value)

    def __get_prep_value(self, value):

        """ Prepare for DB, cast to str """

        return str(value)


class URNListField(URNMixin, models.JSONField):

    """ Store a list of URNs in a charfield

    """

    default_validators = [validate_urn_list]

    def to_python(self, value):

        """ Return list of Models if possible """

        value = super().to_python(value)

        if isinstance(value, list) or value is None:
            return value

        return [self.get_obj(urn) for urn in value]

    def get_obj(self, value):

        """ Return the model from the resource if possible """

        if not isinstance(value, str) or not value:
            return value

        nid = self.get_ns(value)
        _id = self.get_id(value)

        res = ResourceRegistry.get_resource('style', nid)

        return res.get(_id)

    def from_db_value(self, value, *args):

        """ Convert from DB value into python value stored on the model """

        return self.to_python(value)
