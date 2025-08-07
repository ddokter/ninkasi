from django.urls import path, include
from .views import HopDetailView


urlpatterns = [

    path('hopslist_hop/<pk>/',
         HopDetailView.as_view(),
         name="hopslist_view_hop")
]
