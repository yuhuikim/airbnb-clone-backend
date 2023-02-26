from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated

from users.models import User
from . import serializers

class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        # db에 있는 instance로 serializer를 만들고, 
        # user에게서 온 data고
        # 이것들을 serializer에게 주면 알아서 업데이트 해준다.
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            # 새로운 user를 넘겨줌
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class Users(APIView):
    def post(self, request):
        # password가 포함된 data를 받자. --> user가 보낸 password 를 가지고 오는 부분! -- step 1
        password = request.data.get("password")
        if not password:
            raise ParseError
        # serializer은 PrivateUserSerializer를 가져올거고, user가 보낸 data 도 가져온다.
        serializer = serializers.PrivateUserSerializer(data=request.data, )
        if serializer.is_valid():
            user = serializer.save() # db에 저장하는 부분
            # user.password = password # raw password를 그대로 저장하는 방법
            user.set_password(password) # hash화 된 password를 저장하기 위하여
            user.save()
            # 새로운 user를 받는다..!
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else: 
            return Response(serializer.errors)

