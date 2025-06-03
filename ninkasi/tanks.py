"""This module takes care of registering tanks for Ninkasi.

If your own app adds models that are 'tank' like, subclass
ninkasi.Tank. Any subclass of ninkasi.Tank will be picked uo by the
apps module and added to the registry.

"""


class Tank:

    """ Marker class """


class TankRegistry:

    """ Singleton registry for tank types """

    _model_registry = {}
    _registry = {}

    def __new__(cls):

        """ Creator ensuring singleton class """

        if not hasattr(cls, 'instance'):
            cls.instance = super(TankRegistry, cls).__new__(cls)
        return cls.instance

    @classmethod
    def register_model(cls, model_name, model):

        """ Register tank """

        cls._model_registry[model_name] = model

    @classmethod
    def list_tanks(cls):

        """Return a list of tank types, provided by all models and
        instances registered.

        """

        for model in cls._model_registry.keys():
            
            yield model


registry = TankRegistry()
