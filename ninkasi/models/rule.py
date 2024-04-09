"""Rules are used to schedule maintenance for any equipment in the
brewery. A rule can be applied to a task, the combination makes up a
maintenance schedule for a given piece

"""

from django.db import models


class Rule(models.Model):

    """A rule should be able to express things like: within two hours
    after brewing, the brewhouse must be cleaned. Basically, a task
    can be scheduled with a rule. A rule may be specified based on an
    event, but it can also be triggered by a date

    """
