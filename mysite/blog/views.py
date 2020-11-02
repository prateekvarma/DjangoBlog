from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.published.all()
    #Below, the render method takes the (request object, template path, variable to render)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})
