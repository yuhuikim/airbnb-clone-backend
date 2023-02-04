from django.urls import path
# from . import views2
# from . import views3
from . import views

urlpatterns = [
    # path("", views2.categories),
    # path("<int:pk>", views2.category),
    # path("", views3.Categories.as_view()),
    # path("<int:pk>", views3.CategoryDetail.as_view()),
    # ViewSet의 메소드와 사용자가 너한테 보낼 HTTP 메소드를 연결하는 것 밖에 없음
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
