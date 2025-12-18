from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="hello"),
    path("greet/<str:name>", views.greet, name="greet"),
]