from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from post.models import *
from GEL_V2.utils import get_s3_filenames


def home(request):
    post_qs = Post.objects.all().order_by('-created_at')
    post_qs_1 = post_qs[:3]
    post_qs_2 = post_qs[3:6]
    category_qs = Category.objects.all().order_by('name')
    school_logos = get_s3_filenames("green-edu-link-v2", "static/img/schools")
    student_imgs = get_s3_filenames("green-edu-link-v2", "static/img/students/gel_students")

    context = {
        'post_qs_1': post_qs_1,
        'post_qs_2': post_qs_2,
        'category_qs': category_qs,
        'school_logos': school_logos,
        'student_imgs': student_imgs,
    }
    return render(request, "home.html", context)


def about(request):
    category_qs = Category.objects.all().order_by('name')
    context = {
        'category_qs': category_qs,
    }
    return render(request, "about.html", context)


def contact(request):
    category_qs = Category.objects.all().order_by('name')
    context = {
        'category_qs': category_qs,
    }
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
