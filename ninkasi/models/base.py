from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from ..utils import class_implements


class BaseModel(models.Model):

    def get_real(self):

        """See if there is an object there that is the actual
        implementation

        """

        for obj in self._meta.related_objects:

            try:
                real = getattr(self, obj.name)

                if class_implements(real.__class__, self.__class__):
                    return real
            except (ObjectDoesNotExist, AttributeError):
                pass

        return self

    class Meta:
        abstract = True
