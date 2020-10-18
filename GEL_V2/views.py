from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from post.models import *


def home(request):
    post_qs = Post.objects.all().order_by('-created_at')[:3]
    category_qs = Category.objects.all().order_by('name')
    context = {
        'post_qs': post_qs,
        'category_qs': category_qs,
    }
    return render(request, "home.html", context)


def about(request):
    context = {}
    return render(request, "about.html", context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context)


def send_email(request):
    context = {}

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        if name and email and message:
            subject = 'Green Edu Link - Liên hệ từ khách hàng ' + email
            body = """
            Tên khách hàng: {name}

            Email: {email}

            Nội dung: {message}
            """.format(name=name, email=email, message=message)

            try:
                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    ['huynguyen260398@gmail.com', 'tridung2504@gmail.com'],
                    fail_silently=False)

                context['success_msg'] = 'Xin cám ơn! Tin nhắn của bạn đã được gửi thành công!'
            except:
                context['error_msg'] = 'Invalid header found.'
                return render(request, 'contact.html', context)
        else:
            context['error_msg'] = 'Vui lòng điền đầy đủ thông tin!'

    return render(request, 'contact.html', context)


def founder_info(request):
    post_list = Post.objects.all().order_by('-created_at')[:3]
    tag_list = Tag.objects.all()

    context = {
        'post_list': post_list,
        'tag_list': tag_list,
    }
    return render(request, 'founder.html', context)
