from django.urls import path
from .import views

urlpatterns = [
  # path("", views.say_hello),
  # path("", views2.see_all_rooms),
  # path("<int:room_pk>", views2.see_one_room),
  path("", views.Rooms.as_view()),
  path("<int:pk>", views.RoomDetail.as_view()),
  path("amenities/", views.Amenities.as_view()),
  path("amenities/<int:pk>",views.AmenityDetail.as_view()),
       ]