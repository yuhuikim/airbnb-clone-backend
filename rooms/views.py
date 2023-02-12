from django.conf import settings
from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer


"""
Django import 순서(관례)
1. Django와 관련된 것들을 import -> Django package에서 오는 것들을 우선적으로!
2. third-party package를 import 
3. 같은 앱의 것들을 import -> .으로 시작하는 것은 같은 앱, 같은 폴더에 있다는 것
4. 커스텀 app에 관한 것들 import
"""


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


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int("page")
        except ValueError:
            page = 1
        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class Rooms(APIView):
    # IsAuthenticatedOrReadOnly는 인증 받았거나 혹은 읽기 전용 권한이다.
    # GET 요청이면 누구나 통과할 수 있게 해주고, POST, PUT, DELETE 요청이면 오직 인증받은 사람만 통과할 수 있다.
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def post(self, request):
        # 누가 이 url로 요쳥했는지에 관해 많은 정보를 가지고 있음
        # print(dir(request.user))
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            # save(---) 이 괄호에 추가되는 것들은 save를 할 경우 자동으로 create 메서드가 호출되기 때문에
            # create 메서드의 인자인 validated_data에 추가될 것임
            category_pk = request.data.get("category")
            if not category_pk:
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
                    amenities = request.data.get("amenities")
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


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        # 원하는 메소드 어떤 것이든 serializer의 context에 접근할 수 있음 --> serializer에서 self.context 사용하면 context에 접근가능하다.
        # context를 사용하여 serializer 데이터에 데이터를 보낼 수 있음
        serializer = RoomDetailSerializer(
            room,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        # your magic
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoieces.EXPERIENCES:
                        raise ParseError("The Category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    if category_pk:
                        room = serializer.save(category=category)
                    else:
                        room = serializer.save()
                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                            serializer = RoomDetailSerializer(room)
                    else:
                        room.amenities.clear()
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        # 방의 주인이 아니라면 삭제해선 안됨 <-- 확인하려면 로그인이 되어있어야 함
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        # 방의 주인과 request.user의 유저가 같은지 확인하기
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # print(request.query_params)
        try:
            page = request.query_params.get("page", 1)
            # print(type(page)) # <class 'str'>
            page = int("page")
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            # offset --> start, limit --> end
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        # 유저 데이터로부터 오는 페이로드와 평점
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                # + 이 요청을 보내는 유저
                user=request.user,
                # + 우리가 리뷰를 쓰고 있는 방
                room=self.get_object(pk),
            )  # ==> serializer.save를 저장
            # 새로 생성된 리뷰를 받기
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        # PhotoSerializer는 file, description만 갖고 있기 때문에, save를 해주면 file, description만 가진 사진을 만들어낸다.
        # 그러나 사진은 room에 속하는지 experience에 속하는지 알아야한다. 이건 이전에 유저가 방을 만들 때 발생했던 일과 동일하다.
        # 우리는 시리얼라이저에게 방의 주인을 말해줬었음 --> 그렇기때문에 사진이 속한 방도 보내줘야 한다는 뜻임
        if serializer.is_valid():
            photo = serializer.save(room=room)
            # 방과 연결된 사진을 만들어주기 위함
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, reqeust, pk):
        """
        # 1번 방법
        room = self.get_object(pk)
        # 특정 room에 대한 booking 찾기
        bookings = Booking.objects.filter(room=room)

        # 2번 방법 : user가 보낸 pk를 가지는 room에 대한 booking을 찾으면 됨
        bookings = Booking.objects.filter(room__pk=pk)

        user가 보고 있는 room에 대한 예약을 pk를 사용해서 찾을 수 있음
        room__pk에 url을 통해 user가 보낸 pk가 들어가짐 만약에 room에 예약이 없으면 결과는 빈 queryset이 된다.
        또는 받은 pk가 존재하지 않는 room_pk여도 빈 queryset이 반환됨 (즉 존재하지 않는 room)

        user가 존재하지 않는 room에 대한 예약을 요청하면 room이 존재하지 않는다고 알려줄거면
        1번 방법을 사용해야하고, user가 존재하는 room의 pk를 보낼거라고 믿는다면 2번 방법을 사용해서 검색하면 된다.
        1번 방법은 db 조회를 2번하게 되는 것이고, 2번 방법은 1번만 조회하는 것이다.
        그러나 2번 방법은 booking 또는 room이 존재하지 않는 경우 결과값이 동일해서 user는 방자체가 없는 상황임에도 불구하고
        예약이 안된 것이라고 생각할 것이다. 상황에 맞게 쓰면 됨
        relationship(관계)로 filter를 할 때는 room을 먼저 찾아낼 필요는 없다. 즉 1번 처럼 할 필요는 없다.
        """

        room = self.get_object(pk)
        # 현지시간
        now = timezone.localtime(timezone.now()).date()
        # 특정 room에 대한 booking 찾기
        # check_in 날짜가 현재 날짜보다 큰 booking을 찾자! 
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True,)
        return Response(serializer.data)
    
