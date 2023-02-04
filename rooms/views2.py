from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# request 를 써주는 이유는 장고가 request object를 제공함으로써
# 누가 이 페이지를 요청했는지, 어떤 데이터가 전송되고 있는지 등 모든걸 알 수 있다.
# 요청하고 있는 브라우저의 정보, 전송하고 있는 데이터, 요청한 url 정보, ip 주소, 쿠키
# def say_hello(request):
#     # 일반 string을 리턴하면 에러발생
#     # return "hello"
#     return HttpResponse("hello")


def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {"rooms": rooms, "title": "Hello! this title comes from django!"},
    )


def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {"room": room},
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
