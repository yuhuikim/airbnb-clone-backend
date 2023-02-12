from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK
from rooms.models import Room

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


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        # wishlist는 private 한 것이기 때문에 user까지 받아와야하고, url에서 가져오는 id를 가져야하고 그 유저는 이 url로 요청하는 user와 같아야 함
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # 유저가 request.user인 이유는 인증이 되어야만 이 코드를 실행할 수 있기 때문임
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# user가 room의 id를 보내면, wishlist에 room의 id를 추가하도록 할 것임 
# wishlist는 room list랑 experience list가 있음
class WishlistToggle(APIView):
    
    def get_list(self, pk, user):
      try:
          return Wishlist.objects.get(pk=pk, user=user)
      except Wishlist.DoesNotExist:
          raise NotFound
    def get_room(self, pk):
        try:
            return Room.objects.get(pk = pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        '''
        wishlist 모델은 ManyToMany인 rooms 필드, 즉 room의 list를 가지고 있음
        ManyToMany이기 때문에 all 또는 filter를 가지고 있음
        그래서 이렇게 사용할 수 있음 --> wishlist.rooms.all(),wishlist.rooms.filter()
        '''
        # Wishlist 모델에 있는 ManyToMany field의 room의 list로 들어감
        # wishlist 내부의 room list으로 접근해서 filter 하는 것 --> room의 pk랑 일치하는 pk를 갖는 room이 있는지 확인
        # room_pk는 user가 url에 적은 room_pk로 부터 알 수 있음
        if wishlist.rooms.filter(pk=room.pk).exists():
            # room이 wishlist의 rooms에 있으면, 즉 user가 wishlist에서 room을 지우고 싶으면
            wishlist.rooms.remove(room)
        else: 
            # room이 wishlist의 rooms에 없다면, user가 wishlist에서 room을 넣고 싶다는 것!
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)

            
            