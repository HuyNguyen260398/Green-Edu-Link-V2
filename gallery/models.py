from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from datetime import datetime
from bs4 import BeautifulSoup as BSHTML
from GEL_V2.utils import unique_slug_generator, random_string_generator
from post.models import Post


User = settings.AUTH_USER_MODEL


class Picture(models.Model):
    post_id = models.ForeignKey(
        Post, null=True, blank=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(
        upload_to="gallery", height_field=None, width_field=None, max_length=500)
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Post)
def post_post_save_receiver(sender, instance, created, *arg, **kwargs):
    if created:
        soup = BSHTML(instance.content, "html.parser")
        images = soup.findAll('img')

        for image in images:
            img_path = image['src']

            if 'https://green-edu-link-v2.s3.amazonaws.com' in img_path:
                img_path = img_path.replace(
                    'https://green-edu-link-v2.s3.amazonaws.com/media/', '')
                picture = Picture(post_id=instance, image=img_path)
                picture.save()
            # else:
            #     img_path = img_path.replace('/media/', '')


@receiver(pre_save, sender=Picture)
def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, True)


@receiver(post_save, sender=Picture)
def title_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        instance.title = 'img_' + str(instance.pk)
        instance.save()


class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    embed_url = models.URLField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Video)
def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, True)
