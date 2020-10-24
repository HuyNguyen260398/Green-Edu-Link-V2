from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from .forms import CommentForm


def post(request):
    post_qs = Post.objects.all().order_by('-created_at')
    post_qs_filtered = post_qs
    category_qs = Category.objects.all().order_by('name')
    tag_qs = Tag.objects.all().order_by('name')

    paginator = Paginator(post_qs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'post_qs': post_qs,
        'post_qs_filtered': post_qs_filtered,
        'category_qs': category_qs,
        'tag_qs': tag_qs,
        'page_obj': page_obj
    }

    return render(request, "post/post.html", context)


def post_detail(request, id, slug):
    post_obj = Post.objects.get(pk=id)
    post_qs = Post.objects.exclude(pk=id).order_by('-created_at')
    category_qs = Category.objects.all().order_by('name')
    tag_qs = Tag.objects.all().order_by('name')
    comment_qs = Comment.objects.filter(post=post_obj).order_by('-created_on')
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post_obj
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'post_obj': post_obj,
        'post_qs': post_qs,
        'category_qs': category_qs,
        'tag_qs': tag_qs,
        'comment_qs': comment_qs,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    post_obj.comments = comment_qs.count()
    post_obj.views += 1
    post_obj.save()

    return render(request, 'post/post_details.html', context)


def post_search(request):
    post_qs = Post.objects.all().order_by('-created_at')
    category_qs = Category.objects.all().order_by('name')
    tag_qs = Tag.objects.all().order_by('name')
    list_post_id = []

    if request.method == 'GET':
        search_query = request.GET.get('search_query')
        if search_query != '' and search_query is not None:
            posts_tags_qs = PostTag.objects.filter(
                tag_id__name__icontains=search_query)

            if posts_tags_qs.exists():
                for post_tag in posts_tags_qs:
                    post = post_qs.filter(id=post_tag.post_id.id).get()
                    list_post_id.append(post.id)

            post_qs_filtered = post_qs.filter(Q(title__icontains=search_query) |
                                              Q(description__icontains=search_query) |
                                              Q(category__name__icontains=search_query) |
                                              Q(id__in=list_post_id)
                                              ).distinct().order_by('-created_at')
    paginator = Paginator(post_qs_filtered, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'post_qs': post_qs,
        'post_qs_filtered': post_qs_filtered,
        'category_qs': category_qs,
        'tag_qs': tag_qs,
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, "post/post.html", context)


def post_category_search(request, parent='', child=''):
    post_qs = Post.objects.all().order_by('-created_at')
    category_qs = Category.objects.all().order_by('name')
    tag_qs = Tag.objects.all().order_by('name')

    category_obj = None
    sub_category_obj = None

    if child:
        category_obj = category_qs.get(slug=parent)
        sub_category_obj = category_qs.get(slug=child)
        post_qs_filtered = post_qs.filter(
            category__slug__icontains=parent,
            sub_category__slug__icontains=child).order_by('-created_at')
    else:
        category_obj = category_qs.get(slug=parent)
        post_qs_filtered = post_qs.filter(
            category__slug__icontains=parent).order_by('-created_at')

    paginator = Paginator(post_qs_filtered, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'post_qs': post_qs,
        'post_qs_filtered': post_qs_filtered,
        'category_qs': category_qs,
        'category_obj': category_obj,
        'sub_category_obj': sub_category_obj,
        'tag_qs': tag_qs,
        'page_obj': page_obj,
    }

    return render(request, "post/post.html", context)


def post_tag_search(request, slug):
    post_qs = Post.objects.all()
    category_qs = Category.objects.all().order_by('name')
    tag_qs = Tag.objects.all().order_by('name')

    tag_obj = tag_qs.get(slug=slug)

    posts_tags_qs = PostTag.objects.filter(
        tag_id__slug__icontains=slug)

    list_post_id = []
    if posts_tags_qs.exists():
        for post_tag in posts_tags_qs:
            post = post_qs.filter(id=post_tag.post_id.id).get()
            list_post_id.append(post.id)

    post_qs_filtered = post_qs.filter(
        Q(id__in=list_post_id)).distinct().order_by('-created_at')

    paginator = Paginator(post_qs_filtered, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'post_qs': post_qs,
        'post_qs_filtered': post_qs_filtered,
        'category_qs': category_qs,
        'tag_qs': tag_qs,
        'tag_obj': tag_obj,
        'page_obj': page_obj,
    }

    return render(request, "post/post.html", context)
