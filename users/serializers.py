from rest_framework.serializers import ModelSerializer
from .models import User


# room을 볼 때 user를 살짝 보여주기 위해서 만듦
class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )

# 코드 챌린지!!
# 사람들이 내 프로필에서 내 리뷰를 볼 수 있게 한다던지, 내가 얼마나 집을 가지고 있는지, 어떤 도시 여행을 했는지, 나에 대한 리뷰를 볼 수 있게 !
# 이미 사람들이 room에 대한 리뷰를 볼 수 있는 url을 만들었었다. 즉, user에 대한 리뷰를 만들 면 되는 것!
class PublicUserSerializer(ModelSerializer):
    pass