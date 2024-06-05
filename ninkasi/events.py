"""This module takes care of registering events for Ninkasi.

If your own app adds models that either as a model, or as instance,
adds event types, make your model inherit the EventProvider(Model) and
register the model with the EventRegistry.

"""


class EventProviderBase:

    """Define an interface for all periodic things in the brewery,
    like batches, brews, phases, etc. Even non-periodic things may
    provide events however: think of a tank that is emptied.

    """

    @classmethod
    def get_meta_data(cls):

        """ Return metadata for model """

        return getattr(cls, "_meta", None)

    @classmethod
    def list_events(cls):

        """ Return a list of event ID's. Override to get something
        else than start and stop events """

        meta = cls.get_meta_data()

        return [f"{ meta.app_label }.{ meta.model_name }.start",
                f"{ meta.app_label }.{ meta.model_name }.end"]


class EventProvider(EventProviderBase):

    """ Samesame. But different """


class EventProviderModel(EventProviderBase):

    """ Samesame. But different """


class EventRegistry:

    """ Singleton registry for event names """

    _model_registry = {}
    _registry = {}

    def __new__(cls):

        """ Creator ensuring singleton class """

        if not hasattr(cls, 'instance'):
            cls.instance = super(EventRegistry, cls).__new__(cls)
        return cls.instance

    @classmethod
    def register_model(cls, model_name, model):

        """ Register event """

        cls._model_registry[model_name] = model

    @classmethod
    def register(cls, model_name, model):

        """ Register event """

        cls._registry[model_name] = model

    @classmethod
    def list_events(cls):

        """Return a list of event names, provided by all models and
        instances registered.

        """

        for model in cls._model_registry.values():
            for event in model.list_events():
                yield event

        for model in cls._registry.values():
            for instance in model.objects.all():
                for event in instance.list_events():
                    yield event


registry = EventRegistry()
