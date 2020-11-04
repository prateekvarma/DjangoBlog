from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(object_list, 3) #3 posts in pagination
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page not an integer, deliver the first Page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    #Below, the render method takes the (request object, template path, variable to render)
    return render(request,
                  'blog/post/list.html',
                  {'page' : page,
                  'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                            status = 'published',
                            publish__year = year,
                            publish__month = month,
                            publish__day = day)
    return render(request,
                 'blog/post/detail.html',
                 {'post': post})
