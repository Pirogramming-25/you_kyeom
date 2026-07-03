from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class DevTool(models.Model):
    name = models.CharField(max_length=100, verbose_name="개발 툴 이름")
    kind = models.CharField(max_length=100, verbose_name="종류", default="Frontend/Backend") # ➕ 추가
    content = models.TextField(verbose_name="개발 툴 설명", blank=True, null=True)
    
    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    image = models.ImageField(upload_to='idea_thumbnails/', verbose_name="썸네일 이미지")
    content = models.TextField(verbose_name="아이디어 내용")
    interest = models.IntegerField(default=0, verbose_name="관심도")

    devtool = models.ForeignKey(DevTool, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="개발 툴")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LatestIdea(Idea):
    class Meta:
        proxy = True
        ordering = ['-created_at']

class NameOrderedIdea(Idea):
    class Meta:
        proxy = True
        ordering = ['title']

class OldestIdea(Idea):
    class Meta:
        proxy = True
        ordering = ['created_at']

class StarIdeaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(star_count=Count('stars')).order_by('-star_count', '-created_at')

class StarOrderedIdea(Idea):
    objects = StarIdeaManager()

    class Meta:
        proxy = True

class IdeaStar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='stars')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'idea')  #