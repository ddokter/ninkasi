""" Registry for phases """


class PhaseRegistry:

    """ Singleton registry holding possible (meta)phases """

    _registry = {}

    def __new__(cls):

        """ Creator ensuring singleton class """

        if not hasattr(cls, 'instance'):
            cls.instance = super(PhaseRegistry, cls).__new__(cls)
        return cls.instance

    @classmethod
    def register(cls, metaphase):

        """ Register MetaPhase by it's id """

        cls._registry[metaphase.id] = metaphase

    @classmethod
    def get_phase(cls, _id):

        """ Return the named metaphase """

        return cls._registry[_id]

    @classmethod
    def get_phases(cls):

        """ Get all possible phases """

        return cls._registry.values()
