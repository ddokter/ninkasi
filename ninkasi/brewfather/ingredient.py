class Ingredient:

    """Make sure that BrewFather ingredients behave like Model
    instances, so Ninkasi can safely assume all it gets are
    Model-likes.

    """

    def __init__(self, data={}):

        self.data = data

    def __getattr__(self, name):

        try:
            return self.data[name]
        except KeyError as exc:
            raise AttributeError from exc
