from django.shortcuts import render, get_object_or_404, redirect
from .models import Idea, IdeaStar, LatestIdea, NameOrderedIdea, OldestIdea, StarOrderedIdea, DevTool
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.http import JsonResponse

def idea_list(request):
    sort = request.GET.get('sort', 'latest')
    sort_mapping = {
        'latest': LatestIdea, 'stars': StarOrderedIdea, 'name': NameOrderedIdea, 'oldest': OldestIdea,
    }
    selected_model = sort_mapping.get(sort, LatestIdea)
    ideas = selected_model.objects.all()
    paginator = Paginator(ideas, 4) 
    page = request.GET.get('page') 

    try:
        ideas = paginator.page(page)
    except PageNotAnInteger:
        ideas = paginator.page(1)
    except EmptyPage:
        ideas = paginator.page(paginator.num_pages)
    
    
    if request.user.is_authenticated:
        target_user = request.user
    else:
        target_user = User.objects.first() 
        
    user_starred_ideas = []
    if target_user:
        user_starred_ideas = IdeaStar.objects.filter(user=target_user).values_list('idea_id', flat=True)

        
    return render(request, 'ideas/idea_list.html', {
        'ideas': ideas, 
        'sort': sort, 
        'user_starred_ideas': user_starred_ideas
    })


def idea_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        interest = request.POST.get('interest', 0)
        devtool_id = request.POST.get('devtool')
        image = request.FILES.get('image')

        devtool_obj = DevTool.objects.get(id=devtool_id) if devtool_id else None

        new_idea = Idea.objects.create(
            title=title, content=content, interest=interest, devtool=devtool_obj, image=image
        )
        
        return redirect('idea_detail', pk=new_idea.pk)
        
    devtools = DevTool.objects.all()
    return render(request, 'ideas/idea_form.html', {'devtools': devtools})


def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    
    user_starred_ideas = []
    if request.user.is_authenticated:
        user_starred_ideas = IdeaStar.objects.filter(user=request.user).values_list('idea_id', flat=True)
    else:

        first_user = User.objects.first()
        if first_user:
            user_starred_ideas = IdeaStar.objects.filter(user=first_user).values_list('idea_id', flat=True)

    return render(request, 'ideas/idea_detail.html', {
        'idea': idea,
        'user_starred_ideas': user_starred_ideas
    })


def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    if request.method == 'POST':
        idea.title = request.POST.get('title')
        idea.content = request.POST.get('content')
        
        devtool_id = request.POST.get('devtool')
        idea.devtool = DevTool.objects.get(id=devtool_id) if devtool_id else None
        
        
        if request.FILES.get('image'):
            idea.image = request.FILES.get('image')
            
        idea.save()
        return redirect('idea_detail', pk=idea.pk) 
        

    devtools = DevTool.objects.all()
    return render(request, 'ideas/idea_update_form.html', {'idea': idea, 'devtools': devtools})


def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST': 
        idea.delete()
        return redirect('idea_list') 
    return redirect('idea_detail', pk=pk)


def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'ideas/devtool_list.html', {'devtools': devtools})


def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    return render(request, 'ideas/devtool_detail.html', {'devtool': devtool})


def devtool_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        kind = request.POST.get('kind')       
        content = request.POST.get('content') 
        
        new_tool = DevTool.objects.create(name=name, kind=kind, content=content)
        return redirect('devtool_detail', pk=new_tool.pk)
    return render(request, 'ideas/devtool_form.html')


def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    
    if request.method == 'POST':
        devtool.name = request.POST.get('name')
        devtool.kind = request.POST.get('kind')
        devtool.content = request.POST.get('content')
        devtool.save()
        return redirect('devtool_detail', pk=devtool.pk)
        
    return render(request, 'ideas/devtool_update_form.html', {'devtool': devtool})


def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST': 
        devtool.delete()
        return redirect('devtool_list') 
    return redirect('devtool_detail', pk=pk)


def update_interest(request, pk, action):
    idea = get_object_or_404(Idea, pk=pk)
    if action == 'increase':
        idea.interest += 1
    elif action == 'decrease':
        idea.interest -= 1
    idea.save()
    return JsonResponse({
        'status': 'success',
        'interest': idea.interest
        })


def toggle_star(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = User.objects.first() 
        if not current_user:
            current_user = User.objects.create_user(username='guest_user', password='password123')

    star, created = IdeaStar.objects.get_or_create(user=current_user, idea=idea)
    if not created:
        
        star.delete()
        starred = False
    else:
        
        starred = True
        
    return JsonResponse({
        'status': 'success',
        'starred': starred
    })