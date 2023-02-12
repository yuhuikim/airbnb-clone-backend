from rest_framework import  serializers
from .models import Review
from users.serializers import TinyUserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    # 리뷰를 생성할 때, 유저가 누군지 묻지 않고, 페이로드와 평점만 물어봄 
    # 즉, request.data에 유저가 없는 상태로 내 시리얼라이즈가 유효하기 위해선 read_only = True 해야한다.
    user = TinyUserSerializer(read_only = True)
    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating"
        )

'''
TinyUserSerializer 를 사용하면 맨 아래와 같이 표현된다.
   - 사용 전
    {
        "user": 1,
        "payload": "Awesome!",
        "rating": 2
    },
    - 사용 후
    {
        "user": {
            "name": "니꼬",
            "avatar": null,
            "username": "admin"
        },
        "payload": "Awesome!",
        "rating": 2
    },
'''