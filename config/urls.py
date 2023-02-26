"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from rooms import views as room_views
# from users import views as users_views
from django.conf.urls.static import static
# settings 파일을 import 할 수 있게 해줌, settings.py에 대한 프록시
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # path("rooms/",room_views.say_hello),
    path("api/v1/rooms/",include("rooms.urls")),
    path("api/v1/categories/",include("categories.urls")),
    path("api/v1/experiences/",include("experiences.urls")),
    path("api/v1/medias/",include("medias.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),
    path("api/v1/users/", include("users.urls")),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
