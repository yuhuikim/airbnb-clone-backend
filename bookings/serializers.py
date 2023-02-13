from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):
    """
    guests값만 제외하고 모두가 선택옵션이기 때문에 guests만 넘어가도 serializer은 valid 하다고 생각하기 때문에
    추가적인 validation을 해야한다.  아래의 것들이 필수일 수도 있고 선택 값이 될수도 있기 때문에 validation을 직접 추가할 수도 있고,
    새로운 serializer를 만들 수도 있다. 이 경우엔 booking을 생성하는 용도가 될 것 (CreateRoomBookingSerializer 생성하자!)
            "pk",
            "check_in",
            "check_out",
            "experience_time",
    """

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    # room booking 생성만을 위한 serializer
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    # 특정 field의 validation을 커스터마이즈 하고 싶으면 "validate_필드명"으로 method 생성하기!
    # 자동으로 호출해준다. 미친 기능!!
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        # print(value)
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        # print(value)
        return value
