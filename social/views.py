from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from .models import *

# Create your views here.

def log_out(request):
    logout(request)
    return HttpResponse("شما خارج شدید")

def profile(request):
    return HttpResponse("شما وارد شدید")

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(data=request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect('social:profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'registration/edit_user.html', {'user_form': user_form})


def ticket(request):
    send = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}"
            send_mail(cd['subject'], message, 'pythonsabzlearn@gmail.com', ['shanixhunt@gmail.com'],
                      fail_silently=False)
            send = True
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {'forms': form, 'send': send})


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag]).order_by('-created')
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = { 'posts': posts, 'tag': tag }
    return render(request, "social/list.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('social:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:2]
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
    }
    return render(request, 'social/detail.html', context)


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = (Post.objects.annotate(similarity=TrigramSimilarity('tags__name', query))
                .filter(similarity__gt=0.1))
            results2 = (Post.objects
            .annotate(similarity=TrigramSimilarity('description', query))
            .filter(
                Q(similarity__gt=0.1) | Q(description__icontains=query)
            ))
            results = (results1 | results2).order_by('-similarity').distinct()
    context = {'results': results, 'query': query}
    return render(request, 'social/search.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {'post': post, 'comment': comment, 'form': form}
    return render(request, 'forms/comment.html', context)