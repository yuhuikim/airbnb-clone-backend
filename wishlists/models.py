from django.db import models
from common.models import CommonModel

# Create your models here.
class Wishlist(CommonModel):

    """Wishlist Model Definition"""

    name = models.CharField(
        max_length=150,
    )
    # 위시리스트는 많은 방을 가지게 된다.
    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name="wishlists",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        related_name="wishlists",
    )
    # 유저는 많은 위시리스트를 가질 수 있지만, 위시리스트는 한 명의 유저밖에 가지지 못한다.
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wishlists",
    )

    def __str__(self) -> str:
        return self.name
