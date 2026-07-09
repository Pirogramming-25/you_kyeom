from django.urls import path
from . import views

# 다른 앱들과 url 네임스페이스가 겹치는 걸 방지합니다.
app_name = 'pirogram'

urlpatterns = [
    # 1. 메인 피드 페이지 (localhost:8000/)
    path('', views.main_feed, name='main_feed'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # 2. 게시글 작성 페이지 (localhost:8000/post/create/)
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    

    
    # 4. 댓글 작성 기능 (비동기 처리 예정)
    path('post/<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'), # 추가
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    # 5. 좋아요 기능 (비동기 처리 예정)
    path('post/<int:post_id>/like/', views.post_like, name='post_like'),
    
    path('story/create/', views.story_create, name='story_create'),
    path('story/<int:story_id>/delete/', views.story_delete, name='story_delete'),

    path('search/', views.search, name='search'),
    
    path('user/<int:user_id>/follow/', views.user_follow, name='user_follow'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('profile/<int:user_id>/', views.profile_view, name='user_profile'),

]