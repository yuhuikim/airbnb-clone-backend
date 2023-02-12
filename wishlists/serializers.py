from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from rooms.serializers import RoomListSerializer


class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        # serializer.save를 호출하면 아래에 지정한 모델을 받는다!
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )
