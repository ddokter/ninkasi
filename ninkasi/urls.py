from django.contrib import admin
from django.urls import path, include
from .views.auth import LoginView, LogoutView
from .views.base import (DeleteView, ListingView, DetailView, CreateView,
                         UpdateView, InlineCreateView, InlineUpdateView,
                         InlineDeleteView)
from ninkasi.views.batch import BatchCreateView, BatchUpdateView
from ninkasi.views.sample import SampleCreateView
from .views.home import Home


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),

    path('login/',
         LoginView.as_view(),
         name="login"),

    path('logout/',
         LogoutView.as_view(),
         name="logout"),

    path('admin/', admin.site.urls),

    path('', Home.as_view(), name="home"),

    path('batch/add/',
         BatchCreateView.as_view(),
         name="create_batch"),

    path('batch/<int:pk>/edit',
         BatchUpdateView.as_view(),
         name="edit_batch"),

    path('sample/add/',
         SampleCreateView.as_view(),
         name="create_sample"),

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
