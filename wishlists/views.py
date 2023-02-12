from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer

# 기능을 만드는 순서 : url --> views --> config>urls.py에도 추가해주기 --> serializers


class Wishlists(APIView):

    # 위시리스트는 개인용이기 때문임
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save가 호출될 때 모델을 받는다!
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# keyError : 딕셔너리 안에서 뭘 가져오려고 하는데 딕셔너리 안에 그게 없을 경우 발생함!
