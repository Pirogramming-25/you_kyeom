from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pirogram import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pirogram.urls')), 
    path('post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
]

# 🖼️ 유저가 업로드한 이미지(미디어 파일)를 브라우저에서 볼 수 있게 하는 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)