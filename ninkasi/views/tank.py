from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from .base import CreateView, UpdateView
from ..models.tank import Tank
from ..models.task import Task


class TankCreateView(CreateView):

    model = Tank


class TankUpdateView(UpdateView):

    model = Tank
