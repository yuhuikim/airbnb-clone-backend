from django.contrib import admin
from .models import Room, Amenity
# Register your models here.
@admin.action(description="Set all prices to zero")
# admin 액션은 3개의 매개변수로 호출된다.
# 1. 이 액션을 호출하는 클래스
# 2. request 객체 : 이 액션을 누가 호출했는지에 대한 정보를 가지고 있음 --> 이 액션을 호출하는 유저가 슈퍼인지 아닌지 따지는데 사용
# 3. QuerySet : 너가 선택한 모든 객체의 리스트 (queryset 대신에 rooms라고 한다.) 
def  reset_prices(model_admin, request, rooms):
  for room in rooms.all():
      room.price = 0
      room.save()
  # print(model_admin)
  # print(dir(request))
  # print(queryset)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
  
  actions = (reset_prices,)

  list_display = (
    "name",
    "price",
    "kind",
    "total_amenities",
    "rating",
    "owner",
    "created_at",
  )
  list_filter = (
    "country",
    "city",
    "pet_friendly",
    "kind",
    "amenities",
    "created_at",
    "updated_at",
  )

  # self는 관리자 패널에 그대로 나타나기 때문에, 관리자 패널에 있는 모든 메소드는 두번째 매개변수로 room을 갖게하기!
  # def total_amenities(self, room):
  #   return room.amenities.count()

  search_fields = (
    #^는 startswith와 같음, '='는 exact과 같음, 아무것도 적지 않으면 contains
    # "name",
    # "^price",
    # "=price",
    "^owner__username",
  )
  search_help_text = "검색방식에 대한 설명을 검색창 아래에 기재할 수 있다니 엄청나다!"

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
  list_display = (
    "name",
    "description",
    "created_at",
    "updated_at",
  )
  readonly_fields = (
    "created_at",
    "updated_at",
  )
