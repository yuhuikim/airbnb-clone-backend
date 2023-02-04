from django.contrib import admin
from .models import Review

# 필터를 따로 빼서 만들어주는 기능!
# SimpleListFilter은 제목을 필요로 한다. 
class WordFilter(admin.SimpleListFilter):
  title="Filter by Words!"
  parameter_name = "word"
  def lookups(self, request, model_admin):
    return [
      # tuple의 첫번째 값은 url에 나타나고, 두번째 값은 관리자 페이지에 표시된다.
      ("good","Good"),
      ("great","Great"),
      ("awesome","Awesome"),
    ]
  # self를 받아야한다. 왜냐하면 이건 클래스의 메소드이기 때문!
  def queryset(self, request, reviews):
    # 이 필터를 호출한 user를 request로 볼 수 있고, 여기엔 queryset을 받게 될 거다. 
    # 여기서 갖게 될 건 필터링할 review니까 reviews라고 하자. 
    
    # print(request.GET) #-> 아래와 같이쓰면 실제로 url을 읽어서 뽑아내지 않아도 됨!  <QueryDict: {'word': ['good']}>
    word = self.value()
    if word:
      return reviews.filter(payload__contains=word)
    else:
      reviews
# bad 리뷰는 3점 미만이고, good 리뷰는 3점 이상이다. 

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
  # 너의 모델의 str 메서드를 보여주길 원하면, 어드민 모델이 __str__을 적어줄 수 있다. 
  list_display = (
    "__str__",
    "payload",
  )
  list_filter = (
    WordFilter,
    "rating",
    "user__is_host",
    "room__category",
    "room__pet_friendly",
  )
