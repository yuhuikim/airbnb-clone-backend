from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
        # serializer 을 확장해서 다 보여주게 된다.
        # depth = 1


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    # amenities는 amenity의 list여서 many = True 옵션을 줘야함
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Room
        fields = "__all__"
    
    # def create(self, validated_data):
    #     print(validated_data)
    #     return
