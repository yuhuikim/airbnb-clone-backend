from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        # 데이터베이스에 들어갈 value, 관리자 페이지에서 보게되는 label
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = ("won", "Korean Won")
        USD = ("usd", "Dollar")

    # 이름과 성을 덮어쓰기 위함
    # first_name, last_name은 갖기 싫고, name이랑 is_host는 가졌으면 좋겠다!
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    avatar = models.URLField(blank=True)
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        default=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
