""" Ninkasi specific fields """

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from ninkasi.resource import ResourceRegistry
from ninkasi.duration import Duration


RANGE_FIELD_SEP = ","
URN_SEP = ":"


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

    for urn in value:

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

    """ Check whether the value is a Duration object """

    if not value.amount and value.unit:
        raise ValidationError(
            _("Enter a valid tuple of amount/unit"), code="invalid",
            params={"value": value}
        )


class DurationField(models.CharField):

    """ Store tuple of float, str for duration and unit. Unit
    should be one of s, m, h, d. """

    default_validators = [validate_duration]

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

        try:
            kwargs.pop('registry')
        except KeyError:
            pass

        super().__init__(*args, **kwargs)

    def _check_choices(self):

        """ Do not check choices, as they are provided dynamically """

        return []

    def __clean(self, value, model_instance):

        """Sadly Django wants to check on a list of normalized choices
        and we don't. Skip 'validate' call therefore.

        """

        # self.run_validators(value)
        return self.to_python(value)

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

    description = "Resource specifier following the URN scheme."

    # default_validators = [validate_urn]

    def __to_python(self, value):

        """Return Model object if possible.  TODO: this method should
        be very conservative. So check for the correct python result,
        as it may already have been called.

        TODO: enable to_python ???

        """

        if value is None or not isinstance(value, str):
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


class URNListField(URNMixin, models.JSONField):

    """ Store a list of URNs in a charfield

    """

    # default_validators = [validate_urn_list]

    def validate(self, value, model_instance):

        """ The value is a list, and the default validate doesn't support
        multiple values. So override and take care of it. """

        if isinstance(value, list):
            for val in value:
                super().validate(val, model_instance)
        else:
            super().validate(value, model_instance)

    def __to_python(self, value):

        """ Return list of actual URN resource classes if possible """

        value = super().to_python(value)

        if value is None or isinstance(value, str):
            return value

        if isinstance(value, list):

            return [self.get_obj(urn) for urn in value]

    def get_obj(self, value):

        """ Return the model from the resource if possible """

        if not isinstance(value, str) or not value:
            return value

        nid = self.get_ns(value)
        _id = self.get_id(value)

        res = ResourceRegistry.get_resource(self.registry, nid)

        return res.get(_id)

    def from_db_value(self, value, *args):

        """ Convert from DB value into python value stored on the model """

        value = super().from_db_value(value, *args)

        return self.__to_python(value)
