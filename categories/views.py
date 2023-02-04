from django.shortcuts import render
from .models import Category
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
# from django.http import JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers2 import CategorySerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# viewset : https://www.django-rest-framework.org/api-guide/viewsets/#custom-viewset-base-classes

class CategoryViewSet(ModelViewSet):
    # ViewSet에서는 두가지 Property가 필요함
    # 1. serializer가 뭔지 알아야하고
    # 2. ViewSet의 object가 뭔지 알아야함
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


    
