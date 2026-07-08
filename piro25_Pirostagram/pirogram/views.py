# pirogram/views.py
from django.shortcuts import render, redirect, get_object_or_404
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
@login_required(login_url='pirogram:login') # 💡 로그인 안 한 유저가 접근하면 로그인 창으로 안내합니다.
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
    
    # 🔒 보안: 현재 로그인한 사람이 이 글의 작성자가 아니면 메인 피드로 튕겨냅니다.
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

# ❌ 게시글 삭제 뷰
@login_required(login_url='pirogram:login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    # 🔒 보안: 글쓴이 본인만 삭제할 수 있도록 검증합니다.
    if post.author == request.user:
        post.delete()
        return redirect('pirogram:main_feed')
    
    # 🙅‍♂️ 만약 다른 사람이 쓴 글을 주소창으로 강제 접근했다면 삭제 안 하고 그냥 메인 피드로!
    else:
        return redirect('pirogram:main_feed')
        




# 4. 댓글 작성 뷰
def comment_create(request, post_id):
    pass

# 📂 pirogram/views.py 맨 아래에 추가
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

    # 💡 결과를 브라우저 자바스크립트(Ajax)에게 JSON 형태로 돌려줍니다.
    context = {
        'liked': liked,
        'like_count': post.like_users.count()
    }
    return JsonResponse(context)