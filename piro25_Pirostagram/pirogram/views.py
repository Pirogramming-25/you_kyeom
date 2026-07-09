# pirogram/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post, User, Comment, Story
from django.contrib.auth import get_user_model
from django.db.models import Q,Count
User = get_user_model()

from .forms import ProfileUpdateForm

def search(request):
    query = request.GET.get('query', '') # 검색어 가져오기
    users = None
    
    if query:
        users = User.objects.filter(username__icontains=query)
    
    return render(request, 'pirogram/search.html', {
        'users': users,
        'query': query
    })

def post_search_view(request):
    query = request.GET.get('q', '') # 검색창 input의 name='q' 값을 가져옴
    posts = Post.objects.all()
    
    if query:
        # Q 객체를 사용하면 OR(|) 조건으로 여러 필드를 한 번에 검색할 수 있습니다.
        # 내용(content)에 포함되거나, 작성자 이름(username)에 포함된 경우 필터링
        posts = posts.filter(
            Q(content__icontains=query) | 
            Q(author__username__icontains=query)
        ).distinct().order_by('-created_at')
        
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'pirogram/post_search.html', context)

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image') # 📸 프로필 이미지 가져오기
        
        # 유저 중복 체크
        if not User.objects.filter(username=username).exists():
            # 1. 먼저 유저 객체를 생성합니다 (비밀번호 암호화 포함)
            user = User.objects.create_user(username=username, password=password)
            
            # 2. 프로필 이미지가 업로드되었다면 추가로 저장합니다 (필수가 아니므로 if문 처리)
            if profile_image:
                user.profile_image = profile_image
                user.save() # 변경사항 반영
                
            auth_login(request, user) # 가입 완료 후 바로 로그인
            return redirect('pirogram:main_feed')
        else:
            return render(request, 'pirogram/signup.html', {'error': '이미 존재하는 아이디입니다.'})
            
    return render(request, 'pirogram/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # next 파라미터가 있으면 해당 페이지로, 없으면 메인 피드로 이동
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'pirogram:main_feed')
        else:
            return render(request, 'pirogram/login.html', {'error': '아이디 또는 비밀번호가 틀렸습니다.'})
            
    return render(request, 'pirogram/login.html')

#  3. 로그아웃 뷰
def logout_view(request):
    auth_logout(request)
    return redirect('pirogram:main_feed')




# 1. 메인 피드 뷰
def main_feed(request):
    if not request.user.is_authenticated:
        return redirect('pirogram:login') 
    
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'latest')

    following_users = request.user.followings.all()
    target_users = list(following_users) + [request.user]
    posts = Post.objects.filter(author__in=target_users).order_by('-created_at')
    if query:
        posts = posts.filter(
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()
    recommended_users = User.objects.exclude(pk=request.user.pk).order_by('-date_joined')[:5]

    active_stories = Story.objects.order_by('-created_at')
    stories_groups = []
    for user in target_users:
        user_stories = list(Story.objects.filter(author=user).order_by('created_at'))
        if user_stories:
            stories_groups.append({
                'user': user,
                'thumbnail': user_stories[-1],
                'all_stories': user_stories,
                'latest_story_time': user_stories[-1].created_at
            })
    stories_groups.sort(key=lambda x: x['latest_story_time'], reverse=True)
    posts = posts.annotate(
        likes_count=Count('like_users'), 
        comments_count=Count('comments') 
    )

    if sort_by == 'likes':
        # 좋아요 많은 순 -> 같으면 최신순
        posts = posts.order_by('-likes_count', '-created_at')
    elif sort_by == 'comments':
        # 댓글 많은 순 -> 같으면 최신순
        posts = posts.order_by('-comments_count', '-created_at')
    else:
        # 기본값: 최신순
        posts = posts.order_by('-created_at')
    context = {
        'posts': posts,
        'story_groups': stories_groups, 
        'recommended_users': recommended_users,
        'query': query,
        'sort_by': sort_by,
    }
    return render(request, 'pirogram/main_feed.html', context)

# 2. 게시글 작성 뷰 
@login_required(login_url='pirogram:login') # 
def post_create(request):
    if request.method == 'POST':
        image = request.FILES.get('image')     # 업로드된 이미지 파일
        content = request.POST.get('content')   # 입력한 글 본문
        
        if image and content:
            Post.objects.create(
                author=request.user,  # 💡 현재 로그인한 유저가 작성자로 쏙 들어갑니다!
                image=image,
                content=content
            )
            return redirect('pirogram:main_feed') # 성공하면 메인 피드로 이동
            
    return render(request, 'pirogram/post_create.html')

@login_required(login_url='pirogram:login')
def post_update(request, post_id):
    # 1. 수정할 게시글 객체를 가져옵니다. 없으면 404 에러를 띄웁니다.
    post = get_object_or_404(Post, pk=post_id)
    
    # 보안: 현재 로그인한 사람이 이 글의 작성자가 아니면 메인 피드로 튕겨냅니다.
    if post.author != request.user:
        return redirect('pirogram:main_feed')
        
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image') # 새롭게 업로드한 이미지 파일
        
        if content:
            post.content = content # 본문 내용 수정
            if image: 
                post.image = image # 이미지를 새로 넣었을 때만 교체
            post.save() # 데이터베이스에 최종 저장!
            return redirect('pirogram:main_feed') # 완료 후 메인 피드로 이동
            
    # GET 요청 시: 기존 게시글 데이터(post)를 템플릿에 담아서 던져줍니다.
    return render(request, 'pirogram/post_update.html', {'post': post})

#  게시글 삭제 뷰
@login_required(login_url='pirogram:login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.author == request.user:
        post.delete()
        return redirect('pirogram:main_feed')
    
    else:
        return redirect('pirogram:main_feed')
        




#  1. 댓글 작성 (Create)
@login_required(login_url='pirogram:login')
def comment_create(request, post_id):
    
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        if content:
            comment = Comment(
                post=post,
                author=request.user,
                content=content
            )
            if parent_id:
                parent_comment = get_object_or_404(Comment, pk=parent_id)
                comment.parent = parent_comment
            comment.save()
    return redirect('pirogram:main_feed')

#  2. 댓글 수정 (Update)
@login_required(login_url='pirogram:login')
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user and request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
    return redirect('pirogram:main_feed')

#  3. 댓글 삭제 (Delete)
@login_required(login_url='pirogram:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('pirogram:main_feed')


from django.http import JsonResponse

@login_required(login_url='pirogram:login')
def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    # 현재 로그인한 유저가 이 게시글의 like_users에 이미 포함되어 있는지 확인
    if post.like_users.filter(pk=user.pk).exists():
        post.like_users.remove(user) # 이미 좋아요를 눌렀다면 취소
        liked = False
    else:
        post.like_users.add(user) # 안 눌렀다면 좋아요 추가
        liked = True

    # 결과를 브라우저 자바스크립트(Ajax)에게 JSON 형태로 돌려줍니다.
    context = {
        'liked': liked,
        'like_count': post.like_users.count()
    }
    return JsonResponse(context)


@login_required(login_url='pirogram:login')
def story_create(request):
    if request.method == 'POST':
        # HTML input(name="images")에서 여러 파일들을 리스트 형태로 가져옵니다.
        images = request.FILES.getlist('images')
        
        # 받아온 이미지 파일들을 하나씩 순회하며 Story 데이터로 생성 및 저장합니다.
        for img in images:
            Story.objects.create(
                author=request.user,
                image=img
            )
            
    return redirect('pirogram:main_feed')

@login_required(login_url='pirogram:login')
def story_delete(request, story_id):
    if request.method == 'POST':
        # 내가 작성한 스토리 중에서 해당 ID를 가진 스토리를 찾습니다.
        story = get_object_or_404(Story, pk=story_id, author=request.user)
        story.delete() 
        
    return redirect('pirogram:main_feed')


@login_required
def user_follow(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)

    if target_user != request.user:
        if target_user in request.user.followings.all():
            request.user.followings.remove(target_user)
        else:
            request.user.followings.add(target_user)    
            
    return redirect(request.META.get('HTTP_REFERER', 'main_feed'))


@login_required
def profile_view(request, user_id=None):
    if user_id:
        profile_user = get_object_or_404(User, pk=user_id)
    else:
        profile_user = request.user
    
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    followers_count = profile_user.followers.count()
    followings_count = profile_user.followings.count()
    posts_count = posts.count()
    
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'posts_count': posts_count,
        'followers_count': followers_count,
        'followings_count': followings_count,
    }
    return render(request, 'pirogram/profile.html', context)

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        # 파일 업로드(이미지)가 있으므로 request.FILES도 반드시 인자로 넘겨야 합니다.
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('pirogram:profile') # 수정 완료 후 프로필 페이지로 이동
    else:
        # GET 요청 시 기존 유저 데이터가 pre-fill된 폼을 생성
        form = ProfileUpdateForm(instance=request.user)
        
    return render(request, 'pirogram/profile_update.html', {'form': form})

