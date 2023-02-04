from django.db import models
from common.models import CommonModel

# Create your models here.
# 방에는 많은 유저들을 만들 수 있고, 메세지는 한명의 유저로부터 만들어져서 방으로 나간다.
class ChattingRoom(CommonModel):

    """Room Model Definition"""

    users = models.ManyToManyField(
        "users.User",
        related_name="chattingroooms",
    )
    def __str__(self) -> str:
        return "Chatting Room"


class Message(CommonModel):

    """Message Model Definition"""

    text = models.TextField()
    # 메세지는 한명의 유저로부터 생성되고, 유저가 삭제된다고 해서 채팅내역도 사라져야 하는 것은 아님
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
    )
    # 방은 여러개가 있고, 메세지는 한 명의 유저로부터 생성되어 텍스트를 가지고 있다. 그리고 이 메세지는 채팅방으로 간다.
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self) -> str:
       return f"{self.user} says : {self.text}"