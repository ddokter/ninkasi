"""This module takes care of registering milestones for Ninkasi.

If your own app adds models that either as a model, or as instance,
adds milestones, make your model inherit the MilestoneProvider(Model) and
register the model with the MilestoneRegistry.

"""


class MilestoneProviderBase:

    """Define an interface for all periodic things in the brewery,
    like batches, brews, phases, etc. Even non-periodic things may
    provide milestones however: think of a tank that is emptied.

    """

    @classmethod
    def get_meta_data(cls):

        """ Return metadata for model """

        return getattr(cls, "_meta", None)

    @classmethod
    def list_milestones(cls):

        """ Return a list of milestone ID's. Override to get something
        else than start and stop milestones """

        meta = cls.get_meta_data()

        return [f"{ meta.app_label }.{ meta.model_name }.start",
                f"{ meta.app_label }.{ meta.model_name }.end"]


class MilestoneProvider(MilestoneProviderBase):

    """Define interface for providers of milestones that do so per
    instance."""


class MilestoneProviderModel(MilestoneProviderBase):

    """Interface for providers that do so as model."""


class MilestoneRegistry:

    """ Singleton registry for milestone names """

    _model_registry = {}
    _registry = {}

    def __new__(cls):

        """ Creator ensuring singleton class """

        if not hasattr(cls, 'instance'):
            cls.instance = super(MilestoneRegistry, cls).__new__(cls)
        return cls.instance

    @classmethod
    def register_model(cls, model_name, model):

        """ Register milestone """

        cls._model_registry[model_name] = model

    @classmethod
    def register(cls, model_name, model):

        """ Register milestone """

        cls._registry[model_name] = model

    @classmethod
    def list_milestones(cls):

        """Return a list of milestone names, provided by all models and
        instances registered.

        """

        for model in cls._model_registry.values():
            for milestone in model.list_milestones():
                yield milestone

        for model in cls._registry.values():
            for instance in model.objects.all():
                for milestone in instance.list_milestones():
                    yield milestone


registry = MilestoneRegistry()
