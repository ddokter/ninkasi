class ModuleRegistry:

    """ Singleton registry holding resources by it's NID """

    _registry = {}

    def __new__(cls):

        """ Creator ensuring singleton class """

        if not hasattr(cls, 'instance'):
            cls.instance = super(ModuleRegistry, cls).__new__(cls)
        return cls.instance

    @classmethod
    def register(cls, module):

        """ Register resource by it's name """

        cls._registry[module.name] = module

    @classmethod
    def get(cls, name):

        """ Return the named resource """

        return cls._registry[name]

    @classmethod
    def list(cls):

        """ Return the named resources for the given model """

        return cls._registry.values()


registry = ModuleRegistry()
