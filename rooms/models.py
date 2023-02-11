from django.db import models
from common.models import CommonModel


# room.owner.username

# user.rooms
# user.reviews // review.user --> reverse accessor
# user.whishlists

# Create your models here.
class Room(CommonModel):

    """Room model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLATCE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(max_length=180, default="")
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveBigIntegerField()
    rooms = models.PositiveBigIntegerField()
    toilets = models.PositiveBigIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )
    # self를 room이라고 변경해서 사용할 뿐!
    def __str__(room) -> str:
        return room.name

    def total_amenities(room):
        return room.amenities.count()

    # reviews는 related_name : Review 모델에서 room을 가르키는 FK에 부여한 이름!
    # Room 모델에는 review 필드가 없지만, Review 모델에는 room를 FK로 맺고 있기 때문에 가져올 수 있다.
    def rating(room):
        count = room.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            # for review in room.reviews.all(): # 이것보단 아래로 field를 지정해주는 건이 최적화에 훨씬 좋음 - 성능측면
            #     total_rating += review.rating 
            for review in room.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Amenity(CommonModel):

    """Amenity Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
