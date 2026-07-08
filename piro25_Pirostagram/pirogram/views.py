# pirogram/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post, User

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

# 🚪 3. 로그아웃 뷰
def logout_view(request):
    auth_logout(request)
    return redirect('pirogram:main_feed')




# 1. 메인 피드 뷰
def main_feed(request):
    posts = Post.objects.all().order_by('-created_at').prefetch_related('comments')
    return render(request, 'pirogram/main_feed.html', {'posts': posts})

# 2. 게시글 작성 뷰 (에러 원인 해결!)
@login_required # 로그인 상태여야 글을 쓸 수 있음
def post_create(request):
    if request.method == 'POST':
        image = request.FILES.get('image') # 파일 데이터는 request.FILES에서 가져옴
        content = request.POST.get('content')
        
        if image and content:
            Post.objects.create(
                author=request.user, # 현재 로그인한 유저를 작성자로 지정
                image=image,
                content=content
            )
            return redirect('pirogram:main_feed') # 성공 시 메인 피드로 이동
            
    return render(request, 'pirogram/post_create.html')

# 3. 게시글 삭제 뷰
def post_delete(request, post_id):
    pass

# 4. 댓글 작성 뷰
def comment_create(request, post_id):
    pass

# 5. 좋아요 뷰
def post_like(request, post_id):
    pass