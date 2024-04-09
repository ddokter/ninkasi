from django.db import models


class TaskSet(models.Model):

    """Set of tasks, so as to be able to bundle them into a schema,
    to be applied to any equipment.

    """

    tasks = models.ManyToManyField("Task")


    def list_tasks(self):

        """ Return all tasks for this set """

        return self.task_set.all()
