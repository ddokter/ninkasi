""" Provide specific URLs """

from django.conf.urls import url
from .views import RecipeDetailView


urlpatterns = [

    url(r'^recipe/(?P<pk>[\d]+)/?$',
        RecipeDetailView.as_view(),
        name=""
        )
]
