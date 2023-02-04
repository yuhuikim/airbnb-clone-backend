from rest_framework.serializers import ModelSerializer
from .models import Perk

class PerkSerializer(ModelSerializer):
    # serialize 하고 싶은 모델 정의
    class Meta:
        model = Perk
        fields = "__all__"