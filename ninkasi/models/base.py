from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from ..utils import class_implements


class GetRealMixin:

    def get_real(self, done=[]):

        """See if there is an object there that is the actual
        implementation.

        """

        if self in done:
            return self

        _done = done.copy()

        for obj in self._meta.related_objects:

            try:
                real = getattr(self, obj.name)

                if isinstance(real, self.__class__):

                    _done.append(real)

                    return real.get_real(done=_done)
            except (ObjectDoesNotExist, AttributeError):
                pass

        return self
