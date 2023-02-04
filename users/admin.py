from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
# 이 클래스가 user 모델을 관리한다고 선언
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # fieldsets :  model의 field가 보이는 순서를 설정할 수 있게 해줌, field를 넣어서 그 섹션에 제목을 붙일 수도 있음
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password", 
                    "name", 
                    "email", 
                    "is_host",
                    "gender",
                    "language",
                    "currency",
                    ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )
    list_display = ("username", "email", "name", "is_host")
    # fields :
    # fields = ("email","password",'name')
