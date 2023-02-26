from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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
