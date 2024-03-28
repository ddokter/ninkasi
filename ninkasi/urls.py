from django.contrib import admin
from django.urls import path, include
from .views.auth import LoginView, LogoutView
from .views.base import (DeleteView, ListingView, DetailView, CreateView,
                         UpdateView, InlineCreateView, InlineUpdateView,
                         InlineDeleteView)
from .views.batch import (BatchCreateView, BatchUpdateView, BatchDetailView)
from .views.recipe import RecipeCreateView, RecipeUpdateView, RecipeView
from .views.sample import SampleCreateView, SampleUpdateView
from .views.brew import BrewCreateView, BrewUpdateView
from .views.home import Home
from .views.planner import PlannerView
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

    # Generic detail view
    #
    path('batch/<int:pk>',
         BatchDetailView.as_view(),
         name="view"),
    
    path('recipe/add/',
         RecipeCreateView.as_view(),
         name="create_recipe"),

    path('recipe/<int:pk>',
         RecipeView.as_view(),
         name="view"),

    path('recipe/<int:pk>/edit',
         RecipeUpdateView.as_view(),
         name="edit_recipe"),
    
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
