from django.urls import path
from . import views

urlpatterns = [
    path('test-mongo/', views.test_mongo, name='test_mongo'),
    path('exercises/', views.exercises, name='exercises'),
]
