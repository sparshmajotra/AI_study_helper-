from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("document/<int:pk>/", views.document, name="document"),
]
