from django.urls import path
from .views import analyze_video, exercises, test_mongo
from django.http import JsonResponse
from . import views

def api_home(request):
    return JsonResponse({"message": "Welcome to Injury Detection API"})


urlpatterns = [
    path('', api_home, name='api_home'),  # 👈 root /api/ route
    path('exercises/', exercises),
    path('analyze/', analyze_video),
    path('test_mongo/', test_mongo),
]
