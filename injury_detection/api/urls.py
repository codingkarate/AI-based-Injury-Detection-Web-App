from django.urls import path
from . import views

urlpatterns = [
    path("test_mongo/", views.test_mongo, name="test_mongo"),
]
