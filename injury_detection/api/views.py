from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils.db import users

@api_view(['GET'])
def test_mongo(request):
    # Insert a sample user
    users.insert_one({"name": "Amit", "role": "Student"})

    # Fetch data
    data = list(users.find({}, {"_id": 0}))  # exclude _id for JSON safety
    return JsonResponse({"users": data})

