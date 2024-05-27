"""This module defines what a resource looks like and provides a
registry. This allows Ninkasi to use different sources for, for
example, recipes and styles. Resources are registerd to a singleton
registry for a given model, identified by the NID.

The resource acts like a QuerySet in plan Django. Any resource should
return an iterable of objects implementing an interface, like
ninkasi.recipe.BaseRecipe.

"""


class NotFoundInResource(BaseException):

    """ When a get call on the resource cannot deliver the object asked,
    throw this """


class ResourceRegistry:

    """ Singleton registry holding resources by it's NID """

    _registry = {}

    def __new__(cls):

        """ Creator ensuring singleton class """

        if not hasattr(cls, 'instance'):
            cls.instance = super(ResourceRegistry, cls).__new__(cls)
        return cls.instance

    @classmethod
    def register(cls, model, nid, resource):

        """ Register resource byt it's NID """

        if model not in cls._registry:
            cls._registry[model] = {}

        cls._registry[model][nid] = resource

    @classmethod
    def get_resource(cls, model, nid):

        """ Return the named resource """

        return cls._registry[model][nid]

    @classmethod
    def get_resources(cls, model):

        """ Return the named resources for the given model """

        return cls._registry[model].values()


class Resource:

    name = ""

    def list(self):

        """ Return an iterable of the objects queried """

    def get(self, _id):

        """Get the resource by it's id. Throw NotFoundInResource if
        nothing is found.

        """


class ModelResource(Resource):

    """Django resource, returning models the usual way. If you need
    more elaborate stuff, go ahead and do something similar to this.

    """

    name = "django"
    model = None

    def __init__(self, model):

        self.model = model

    def list(self):

        return self.model.objects.all()


registry = ResourceRegistry()
