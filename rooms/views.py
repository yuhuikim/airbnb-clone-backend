from rest_framework.views import APIView
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from categories.models import Category
from django.db import transaction

class Amenities(APIView):
    # 모든 view function 은 request를 받는다.
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializers = AmenitySerializer(all_amenities, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            # ModelSerializer가 자동으로 amenity를 만들게 해야함
            amenity = serializer.save()

            # 우리는 당연히 serialize 해줘야 함
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    # pk를 갖는 amenity를 찾거나 404 Not Found를 보여주는데, 이 작업의 반복을 막기 위해서 만듦
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        # DB에서 가져온 amenity와 사용자가 보낸 데이터인 request.data를 보내고, 부분적 업데이트라는 것을 parital 로 알려줌
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # 누가 이 url로 요쳥했는지에 관해 많은 정보를 가지고 있음
        # print(dir(request.user))

        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                # save(---) 이 괄호에 추가되는 것들은 save를 할 경우 자동으로 create 메서드가 호출되기 때문에
                # create 메서드의 인자인 validated_data에 추가될 것임
                category_pk = request.data.get("category")
                if not category_pk :
                    # ParseError는 request가 잘못된 데이터를 가지고 있을 때 발생
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoieces.EXPERIENCES:
                        raise ParseError("The Category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                try:
                    # transaction.atomic이 없을 떈, 코드를 실행할 때마다, 쿼리가 즉시 DB에 반영됨
                    # 도중에 에러가 발생한다면, 그 변경사항들을 DB에 반영하지 않는다.
                    # try-except 구문을 transaction 내부엔 사용하면 에러난 사실을 모르기 때문에 사용하지 않음
                    with transaction.atomic():
                        room = serializer.save(owner=request.user, category=category)
                        amenities = request.data.get('amenities')
                        # ManytoMany 필드가 작동하는 방법임
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
            else: 
                return Response(serializer.errors)
        else: 
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_room = serializer.save()
            return Response(
                AmenitySerializer(updated_room).data,
            )
        else:
            return Response(serializer.errors)       

    def delete(self, request, pk):
        room = self.get_object(pk)
        # 방의 주인이 아니라면 삭제해선 안됨 <-- 확인하려면 로그인이 되어있어야 함
        if not request.user.is_authenticated:
            raise NotAuthenticated
        # 방의 주인과 request.user의 유저가 같은지 확인하기
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
