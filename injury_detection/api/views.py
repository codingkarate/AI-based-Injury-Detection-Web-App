from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from pymongo import MongoClient
from .utils.pose_estimator import analyze_video


# ✅ Root API endpoint
def api_home(request):
    return HttpResponse("Welcome to Injury Detection API")


# ✅ MongoDB connection test
def test_mongo(request):
    try:
        client = MongoClient("mongodb://localhost:27017/")  # Change if using Atlas or other URI
        db = client["injury_detection_db"]  # Example DB name
        collection_names = db.list_collection_names()
        return JsonResponse({"status": "success", "collections": collection_names})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


# ✅ Exercise list endpoint
def exercises(request):
    data = [
        {"id": 1, "name": "Jumping Squats"},
        {"id": 2, "name": "Lunges"},
        {"id": 3, "name": "Pushups"},
    ]
    return JsonResponse({"exercises": data})


# ✅ Video analysis endpoint
@csrf_exempt
@api_view(['POST'])
def analyze_video_view(request):  # ⚠ renamed to avoid clash with imported function
    parser_classes = (MultiPartParser, FormParser)
    if 'video' not in request.FILES:
        return Response({'error': 'No video file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    video_file = request.FILES['video']

    # Save uploaded video temporarily
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        for chunk in video_file.chunks():
            temp_video.write(chunk)
        temp_video_path = temp_video.name

    try:
        result = analyze_video(temp_video_path)  # imported from pose_estimator.py
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
