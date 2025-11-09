from django.urls import path
from .views import analyze_video, exercises, test_mongo

urlpatterns = [
    path('exercises/', exercises),
    path('analyze/', analyze_video),
    path('test_mongo/', test_mongo),
]
