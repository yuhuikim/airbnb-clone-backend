from django.shortcuts import render
from .models import Category
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
# from django.http import JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers2 import CategorySerializer

# Create your views here.
@api_view(["GET", "POST"])
def categories(reqeuest):
    if reqeuest.method == "GET":
        all_categories = Category.objects.all()
        # return JsonResponse(
        #     {
        #         "ok": True,
        #         "categories": serializers.serialize("json", all_categories),
        #     },
        # )
        # 하나의 카테고리를 위한 serializer인데 카테고리 리스트를 보냈으니, 많은 카테고리를 보낸다고 many=True로 알려준다.
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    elif reqeuest.method == "POST":
        # serializer을 가져다가 사용자가 보낸 데이터를 넘겨주는 것으로  "serializer = CategoryServiallerzer(category)"과는 다르다.
        # request.data로 CategorySerializer를 만들기
        serializer = CategorySerializer(data=reqeuest.data)
        if serializer.is_valid():
            # serializer.save() --> save()를 실행하면 serializer은 자동으로 create 메서드를 찾기 시작한다. 그 객체의 생성을 다루는건 우리가 해야함

            # python 객체
            new_category = serializer.save()

            # JSON으로 번역하여 return
            return Response(
                CategorySerializer(new_category).data,
            )
        else:
            return Response(serializer.errors)

        # user가 우리에게 보내고 있는 내용을 볼 수 있음 e.g. {'name': 'Category from DRF', 'kind': 'rooms'}
        # print(
        #     reqeuest.data
        # )

        # 이렇게 생성하게 된다면 길이 제한과 같은 검증을 거치지 않고 user는 아무렇게나 insert 가능해서 별로다.
        # --> 검증이 필요함! is_valid 사용하자.
        # Category.objects.create(name=reqeuest.data["name"], kind=reqeuest.data["kind"])


# serialize은 python 객체를 json으로 변환
# request 객체는 url에서 호출된 모든 함수에게 주어짐


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        # DB에서 가져온 category로 CategorySerializer 만들기
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == "PUT":
        # 데이터베이스로부터 가져온 category랑 사용자의 데이터로 serializer을 생성!
        serializer = CategorySerializer(
            category,
            data=request.data,
            # 부분적으로 업데이트 해주기 위하여 아래의 옵션쓰기
            # 사용자한테 받지 못한 데이터는 현재 데이터베이스에 있는 정보로 유지하기
            partial=True,
        )
        if serializer.is_valid():
            update_category = serializer.save()
            return Response(
                CategorySerializer(update_category).data,
            )
        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# {
#     "name":"Category from DRF",
#     "kind":"rooms"
# }
