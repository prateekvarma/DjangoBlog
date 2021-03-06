from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.

#def post_list(request):
#    object_list = Post.published.all()
#    paginator = Paginator(object_list, 3) #3 posts in pagination
#    page = request.GET.get('page')
#    try:
#        posts = paginator.page(page)
#    except PageNotAnInteger:
#        #if page not an integer, deliver the first Page
#        posts = paginator.page(1)
#    except EmptyPage:
#        #if page is out of range, deliver last page of results
#        posts = paginator.page(paginator.num_pages)
#    #Below, the render method takes the (request object, template path, variable to render)
#    return render(request,
#                  'blog/post/list.html',
#                  {'page' : page,
#                  'posts': posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                            status = 'published',
                            publish__year = year,
                            publish__month = month,
                            publish__day = day)

    # List of active comments for this post
    #The .comments. below is "related_name='comments'" from Comments model to refer to the relationship
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment object, but not store in DB yet
            new_comment = comment_form.save(commit=False)
            # Assign the related post to comment
            new_comment.post = post
            #save comment to DB
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                 'blog/post/detail.html',
                 {'post': post,
                 'comments': comments,
                 'new_comment': new_comment,
                 'comment_form': comment_form})

def post_share(request, post_id):
    #retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
            return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
    else:
        form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
