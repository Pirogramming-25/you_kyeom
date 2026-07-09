from django.db import models
from django.contrib.auth.models import AbstractUser # 변경: 기본 User 대신 AbstractUser 상속
from django.conf import settings
# 1. 커스텀 유저 모델 정의
class User(AbstractUser):
    # Django 기본 유저 필드(username, password, email 등)는 자동으로 포함됩니다.
    # 인스타그램에 필요한 필드만 추가합니다.
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    followings = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='followers', 
        blank=True
    )
    def __str__(self):
        return self.username


# 2. 게시글 모델
class Post(models.Model):
    # 중요: 이제 User는 위에서 정의한 커스텀 User 모델을 가리킵니다.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/%Y/%m/%d/')
    content = models.TextField()
    like_users = models.ManyToManyField(User, related_name='like_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username}의 게시글 - {self.content[:10]}'


# 3. 댓글 모델
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )

    def __str__(self):
        return f'{self.author.username}: {self.content[:10]}'
    
class Story(models.Model):
    # 👤 스토리를 올린 사람 (유저 모델과 연결)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    
    # 📸 스토리 이미지 파일
    image = models.ImageField(upload_to='stories/')
    
    # ⏰ 올린 시간 (인스타처럼 24시간 뒤에 지우는 로직 등을 짤 때 기준점이 됩니다)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}의 스토리 ({self.created_at})"