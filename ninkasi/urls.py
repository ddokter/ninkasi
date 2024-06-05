from django.contrib import admin
from django.urls import path, include
from .views.auth import LoginView, LogoutView
from .views.base import (DeleteView, ListingView, DetailView, CreateView,
                         UpdateView, InlineCreateView, InlineUpdateView,
                         InlineDeleteView)
from .views.batch import (BatchCreateView, BatchDetailView,
                          BatchImportPhasesView, BatchMeasurements)
from .views.recipe import RecipeDetailView, RecipeListingView
from .views.style import StyleListingView
from .views.sample import SampleCreateView, SampleUpdateView
# from .views.measurement import MeasurementCreateView
from .views.brew import (BrewDetailView, BrewCreateView, BrewUpdateView,
                         BrewImportPhasesView)
from .views.phase import (PhaseMoveStepView, PhaseView, AddPhaseView,
                          MovePhaseView)
from .views.beer import BeerCreateView, BeerUpdateView
from .views.home import Home, FixTask
from .views.planner import PlannerView
from .views.agenda import AgendaView
from .views.transfer import TransferView


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),

    path('brewfather/', include('ninkasi.brewfather.urls')),

    path('login/',
         LoginView.as_view(),
         name="login"),

    path('logout/',
         LogoutView.as_view(),
         name="logout"),

    path('planner/',
         PlannerView.as_view(),
         name="planner"),

    path('agenda/',
         AgendaView.as_view(),
         name="agenda"),

    path('transfer/<int:ct>/<int:cid>/',
         TransferView.as_view(),
         name="transfer"),

    path('transfer/',
         TransferView.as_view(),
         name="transfer"),

    path('admin/', admin.site.urls),

    path('', Home.as_view(), name="home"),

    path('task/fix/<int:task>/',
         FixTask.as_view(),
         name="fixtask"),

    path('batch/add/',
         BatchCreateView.as_view(),
         name="create_batch"),

    path('batch/add/<int:beer>/',
         BatchCreateView.as_view(),
         name="create_batch"),

    path('batch/<int:pk>',
         BatchDetailView.as_view(),
         name="view"),

    path('batch/<int:pk>/measurements',
         BatchMeasurements.as_view(),
         name="batch_measurements"),

    path('batch/<int:pk>/importphases',
         BatchImportPhasesView.as_view(),
         name="batch_import_phases"),

    path('recipe/<int:pk>',
         RecipeDetailView.as_view(),
         name="view"),

    path('recipe/list',
         RecipeListingView.as_view(),
         name="list_recipes"),

    path('style/list',
         StyleListingView.as_view(),
         name="list_styles"),

    path('sample/add/',
         SampleCreateView.as_view(),
         name="create_sample"),

    path('sample/<int:pk>/edit',
         SampleUpdateView.as_view(),
         name="edit_sample"),

    path('sample/add/<int:batch>',
         SampleCreateView.as_view(),
         name="create_sample"),

    path('brew/<int:pk>',
         BrewDetailView.as_view(),
         name="view"),

    path('brew/add/',
         BrewCreateView.as_view(),
         name="create_brew"),

    path('brew/add/<int:batch>',
         BrewCreateView.as_view(),
         name="create_brew"),

    path('brew/<int:pk>/edit',
         BrewUpdateView.as_view(),
         name="edit_brew"),

    path('brew/<int:pk>/importphases',
         BrewImportPhasesView.as_view(),
         name="brew_import_phases"),

    path('beer/add/',
         BeerCreateView.as_view(),
         name="create_beer"),

    path('beer/<int:pk>/edit',
         BeerUpdateView.as_view(),
         name="edit_beer"),

    path('phase/<int:pk>',
         PhaseView.as_view(),
         name="view"),

    path('phase/<int:pk>/movestep/<int:step>',
         PhaseMoveStepView.as_view(),
         name="phase_movestep"),

    path('<str:model>/<int:pk>/addphase/<str:phase>',
         AddPhaseView.as_view(),
         name="addphase"),

    path('<str:model>/<int:pk>/movephase/<int:phase>',
         MovePhaseView.as_view(),
         name="movephase"),

    path('<str:model>/<int:pk>/addstep/<int:phase>/<str:step>',
         AddPhaseView.as_view(),
         name="addstep"),

    # Tank
    #
    # path('tank/add/<int:batch>',
    #     TankCreateView.as_view(),
    #     name="create_tank"),

    # path('tank/<int:pk>/edit',
    #     TankUpdateView.as_view(),
    #     name="edit_tank"),


    # Generic delete view
    #
    path('<str:model>/<int:pk>/delete',
         DeleteView.as_view(),
         name="delete"),

    # Generic listing
    #
    path('<str:model>/list',
         ListingView.as_view(),
         name="list"),

    # Generic detail view
    #
    path('<str:model>/<int:pk>',
         DetailView.as_view(),
         name="view"),

    # Generic add view
    #
    path('<str:model>/add/',
         CreateView.as_view(),
         name="create"),

    # Generic edit view
    #
    path('<str:model>/<int:pk>/edit',
         UpdateView.as_view(),
         name="edit"),

    # Generic inline add
    #
    path('<str:parent_model>/<int:parent_pk>/add_<str:model>',
         InlineCreateView.as_view(),
         name="inline_create"),

    # Generic inline edit
    #
    path('<str:parent_model>/<int:parent_pk>/edit_<str:model>/<int:pk>',
         InlineUpdateView.as_view(),
         name="inline_edit"),

    # Generic inline delete
    #
    path('<str:parent_model>/<int:parent_pk>/rm_<str:model>/<int:pk>',
         InlineDeleteView.as_view(),
         name="inline_delete"),

]
