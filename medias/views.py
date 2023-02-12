from django.shortcuts import render
from rest_framework.views import APIView
from .models import Photo
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated


class PhotoDetail(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        # 사진을 업로드한 사람이 사진의 room의 주인인지 혹은 experience의 주인인지 확인해야함
        if (photo.room and photo.room.owner != request.user) or (photo.experience and photo.experience.host != request.user):
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)

