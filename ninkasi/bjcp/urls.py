from django.urls import path, include
from .views import StyleView


urlpatterns = [

    path('bjcp_style/<pk>',
         StyleView.as_view(),
         name="bjcp_view_style")
]
