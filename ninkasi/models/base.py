from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from ..utils import class_implements


class BaseModel(models.Model):

    def get_real(self, done=[]):

        """See if there is an object there that is the actual
        implementation

        """

        if self in done:
            return self

        for obj in self._meta.related_objects:

            try:
                real = getattr(self, obj.name)

                if class_implements(real.__class__, self.__class__):

                    done.append(real)

                    return real.get_real(done=done)
            except (ObjectDoesNotExist, AttributeError):
                pass

        return self

    class Meta:
        abstract = True
