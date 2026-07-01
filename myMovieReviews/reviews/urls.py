from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review_list'),                  # Read (전체 목록)
    path('<int:pk>/', views.review_detail, name='review_detail'),    # Read (상세 보기)
    path('create/', views.review_create, name='review_create'),      # Create (작성)
    path('<int:pk>/update/', views.review_update, name='review_update'), # Update (수정)
    path('<int:pk>/delete/', views.review_delete, name='review_delete'), # Delete (삭제)
]