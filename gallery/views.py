from django.shortcuts import render
from django.core.paginator import Paginator

from .models import *
from post.models import *


def gallery(request):
    return render(request, 'gallery/gallery.html')


def picture_gallery(request):
    picture_qs = Picture.objects.all().order_by('-timestamp')
    category_qs = Category.objects.all().order_by('name')
    context = {
        'category_qs': category_qs,
    }
    if picture_qs.exists():
        paginator = Paginator(picture_qs, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['picture_qs'] = picture_qs
        context['page_obj'] = page_obj
    return render(request, 'gallery/picture_gallery.html', context)


def video_gallery(request):
    video_qs = Video.objects.all().order_by('-timestamp')
    category_qs = Category.objects.all().order_by('name')
    context = {
        'category_qs': category_qs,
    }
    if video_qs.exists():
        paginator = Paginator(video_qs, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['video_qs'] = video_qs,
        context['page_obj'] = page_obj
    return render(request, 'gallery/video_gallery.html', context)
