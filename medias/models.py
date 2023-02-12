from django.db import models
from common.models import CommonModel

# Create your models here.
class Photo(CommonModel):
    file = models.URLField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    def __str__(self) -> str:
      return "Photo File"


class Video(CommonModel):
    file = models.URLField()
    # OneToOneField는 Foreignkey와 같지만 고유한 값이 된다.
    # 하나의 활동과 연결된다면 그 활동은 다른 동영상을 가질 수 없다는 뜻 > 모델 간의 연결을 고유하게 만들 수 있음
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )
    def __str__(self) -> str:
        return "Video File"