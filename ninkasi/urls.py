from django.contrib import admin
from django.urls import path, include
from .views.auth import LoginView, LogoutView
from .views.base import (DeleteView, ListingView, DetailView, CreateView,
                         UpdateView, InlineCreateView, InlineUpdateView,
                         InlineDeleteView)
from .views.batch import (BatchCreateView, BatchUpdateView, BatchDetailView,
                          BatchImportPhasesView)
from .views.recipe import (RecipeCreateView, RecipeUpdateView, RecipeView,
                           RecipeAddPhaseView, RecipeMovePhaseView,
                           RecipeListingView)
from .views.style import StyleListingView
from .views.sample import SampleCreateView, SampleUpdateView
from .views.brew import (BrewCreateView, BrewUpdateView, BrewImportPhasesView)
from .views.phase import PhaseMoveStepView, PhaseView
from .views.beer import BeerCreateView
from .views.home import Home
from .views.planner import PlannerView
from .views.agenda import AgendaView
from .views.transfer import TransferView


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),

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

    path('batch/add/',
         BatchCreateView.as_view(),
         name="create_batch"),

    path('batch/add/<int:beer>/',
         BatchCreateView.as_view(),
         name="create_batch"),

    path('batch/<int:pk>/edit',
         BatchUpdateView.as_view(),
         name="edit_batch"),

    path('batch/<int:pk>',
         BatchDetailView.as_view(),
         name="view"),

    path('batch/<int:pk>/importphases',
         BatchImportPhasesView.as_view(),
         name="batch_import_phases"),

    path('recipe/add/',
         RecipeCreateView.as_view(),
         name="create_recipe"),

    path('recipe/<int:pk>',
         RecipeView.as_view(),
         name="view"),

    path('recipe/<int:pk>/edit',
         RecipeUpdateView.as_view(),
         name="edit_recipe"),

    path('recipe/<int:pk>/addphase/<str:phase>',
         RecipeAddPhaseView.as_view(),
         name="recipe_addphase"),

    path('recipe/<int:pk>/movephase/<int:phase>',
         RecipeMovePhaseView.as_view(),
         name="recipe_movephase"),

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

    path('phase/<int:pk>',
         PhaseView.as_view(),
         name="view"),

    path('phase/<int:pk>/movestep/<int:step>',
         PhaseMoveStepView.as_view(),
         name="phase_movestep"),

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
