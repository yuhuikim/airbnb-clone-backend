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
        serializer = serializers.PrivateUserSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            user = serializer.save()  # db에 저장하는 부분
            # user.password = password # raw password를 그대로 저장하는 방법
            user.set_password(password)  # hash화 된 password를 저장하기 위하여
            user.save()
            # 새로운 user를 받는다..!
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# http://127.0.0.1:8000/api/v1/users/@admin1
class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    # 인증되지 않은 user가 호출하지 못하도록 막기
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        # 유튜브 : 노마드 코더 비밀번호 해쉬" 영상 참고하기
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            # set_password는 new_password를 hash 할 때만 작동
            user.set_password(new_password)
            # 그러니까 아래의 작업이 꼭 필요하다.. --> 왜?
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        # username과 password이 같으면 user가 나옴!
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        # user를 찾으면 request 객체와 login 함수를 호출하면 된다.
        if user:
            # login 함수를 호출하면 장고에서는 user를 로그인 시키고, 백엔드에서는 user가 담긴 세션을 생성하고, 사용자에게 쿠키를 보내준다.
            login(
                request,
                user,
            )
            return Response({"ok":"Welcome!"})
        else:
            return Response({"error": "wrong password"})

class LogOut(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(({"ok":"GoodBye"}))