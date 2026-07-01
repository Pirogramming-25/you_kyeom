from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')), # 모든 요청을 reviews 앱의 urls로 전달
]