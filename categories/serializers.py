from rest_framework import serializers
from .models import Category

# ModelSerializer는 일반적인 Serializer로 기본적인 create, update 빼고, 자동으로 model의 field를 파악한다.
class CategorySerializer(serializers.ModelSerializer):

    # serializer가 category model을 위한 serializer를 만들어준다.
    class Meta:
        model = Category
        # 제외하고 싶은 필드가 있으면 아래와 같이 함
        # exclude = (
        #     "created_at"
        # )
        # 모든 필드를 보여주고 싶으면 아래와 같이 함
        fields = (
            "name",
            "kind",
        )
