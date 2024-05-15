from django.urls import path, include
from .views import RecipeView


urlpatterns = [

    path('brewfather_recipe/<pk>',
         RecipeView.as_view(),
         name="brewfather_view_recipe")
]
