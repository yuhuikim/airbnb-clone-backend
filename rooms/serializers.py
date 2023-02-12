from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from rest_framework import serializers
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )
        # serializer 을 확장해서 다 보여주게 된다.
        # depth = 1

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        # 시리얼라이저의 context에서 request 객체를 가져오는 것
        # class Rooms에 보면 context={"request": request,} 를 써서 request 객체를 보내주고 있음
        request = self.context["request"]
        # 방의 owner가 요청을 보낸 유저랑 같은지 아닌지에 따라서 true, false로 반환함
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    # amenities는 amenity의 list여서 many = True 옵션을 줘야함
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    # SerializerMethodField은 potato의 값을 계산할 Method를 만든다는 것임
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    # RoomDetailSerializer가 reviews라는 새로운 필드를 가진다. --> 같은 방을 가리키는 리뷰가 많을 수 있으니 many=True
    # 리뷰들을 다 불러오면 db가 죽을 수 있기 때문에 제거!
    # reviews = ReviewSerializer(
    #     read_only=True,
    #     many=True,
    # )
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    # 이름을 get_속성 ==> 메소드 명 라고 해줘야함 (무조건)
    # 시리얼라이즈 하고 있는 오브젝트와 함께 호출
    def get_rating(self, room):
        # print(self.context)
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        # 방의 owner가 요청을 보낸 유저랑 같은지 아닌지에 따라서 true, false로 반환함
        return room.owner == request.user

    # def create(self, validated_data):
    #     print(validated_data)
    #     return

    def get_is_liked(self, room):
        request = self.context["request"]
        # request.user가 갖고있는 wishlist를 찾아와야함
        # room을 보고있는 user가 소유한 wishlists를 찾는 것, 즉 room_list 안에 그 room을 가지고 있는 wishlist를 찾아냄
        # user가 만든 wishlist 중에 room_id가 있는 room list를 포함한 wishlist를 찾음
        # filter는 array 결과로 주기 때문에 T/F로 반환받기 위해 exists를 사용!
        wish = Wishlist.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
        ).exists()
        return wish
