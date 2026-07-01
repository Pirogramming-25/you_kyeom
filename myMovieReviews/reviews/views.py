from django.shortcuts import render, redirect, get_object_or_404
from .models import MovieReview

# READ (전체 목록)
def review_list(request):
    sort_by = request.GET.get('sort', '-created_at')
    
    if sort_by == 'title':
        reviews = MovieReview.objects.all().order_by('title')          # 제목 이름 순
    elif sort_by == 'rating':
        reviews = MovieReview.objects.all().order_by('-rating')        # 별점 높은 순
    elif sort_by == 'running_time':
        reviews = MovieReview.objects.all().order_by('running_time')  # 상영 시간 짧은 순
    else:
        reviews = MovieReview.objects.all().order_by('-created_at')    # 최신 등록 순
    
    for review in reviews:
        if review.running_time:
            hours = review.running_time // 60
            minutes = review.running_time % 60
            review.converted_time = f"{hours}시간 {minutes}분" if hours > 0 else f"{minutes}분"
        else:
            review.converted_time = "정보 없음"

    return render(request, 'reviews/review_list.html', {'reviews': reviews, 'current_sort': sort_by})

# READ (상세 보기)
def review_detail(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)

    if review.running_time:
        hours = review.running_time // 60
        minutes = review.running_time % 60
        converted_time = f"{hours}시간 {minutes}분" if hours > 0 else f"{minutes}분"
    else:
        converted_time = "정보 없음"
        
    return render(request, 'reviews/review_detail.html', {
        'review': review, 
        'converted_time': converted_time # 변환된 글자 전달
    })

    return render(request, 'reviews/review_detail.html', {'review': review})

# CREATE (리뷰 작성)
def review_create(request):
    if request.method == 'POST':
        MovieReview.objects.create(
            title=request.POST['title'],
            release_year=request.POST['release_year'], # 👈 추가!
            director=request.POST['director'],
            actor=request.POST['actor'],
            genre=request.POST['genre'],
            rating=request.POST['rating'],
            running_time=request.POST['running_time'],
            content=request.POST['content']
        )
        return redirect('reviews:review_list')
    return render(request, 'reviews/review_form.html')

# UPDATE (리뷰 수정)
def review_update(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)
    if request.method == 'POST':
        review.title = request.POST['title']
        review.release_year = request.POST['release_year'] # 👈 추가!
        review.director = request.POST['director']
        review.actor = request.POST['actor']
        review.genre = request.POST['genre']
        review.rating = request.POST['rating']
        review.running_time = request.POST['running_time']
        review.content = request.POST['content']
        review.save()
        return redirect('reviews:review_detail', pk=pk)
    return render(request, 'reviews/review_form.html', {'review': review})

# DELETE (리뷰 삭제)
def review_delete(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('reviews:review_list')
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})