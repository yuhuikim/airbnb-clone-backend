from django.db import models
from common.models import CommonModel

'''
A-FK
B.A_set
만약 모델 A가 모델 B에 대한 FK를 가지고 있다면,
모델 B는 자동적으로 A_set이라는 역접근자를 받는다.
그리고 A_set은 모델 B에게 그를 가리키고 있는 모델 A의 모든 것을 준다.
A_set 으로 쓰지 않고, related_name을 사용! 이걸 가리키는 모든 것에 접근하는 방법을 명시한다.
'''

class Review(CommonModel):

    """Review from a User to a Room or Experience"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    # room은 역접근자(reverse accessor)를 사용함으로서 어떤 리뷰가 자기를 가리키고 있는지 알 수 있다.
    # 역접근자는 room.reviews.all() 이다.
    room = models.ForeignKey(
      "rooms.Room",
      null=True,
      blank=True,
      on_delete=models.CASCADE,
      related_name="reviews",

    )
    experience = models.ForeignKey(
      "experiences.Experience",
      null=True,
      blank=True,
      on_delete=models.CASCADE,
      related_name="reviews",

    )
    payload = models.TextField()
    rating = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐️"
    
