from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from GEL_V2.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post:post_category_search', kwargs={'slug': self.slug})


@receiver(pre_save, sender=Category)
def slug_pre_save_receiver_category(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, False)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post:post_tag_search', kwargs={'slug': self.slug})


@receiver(pre_save, sender=Tag)
def slug_pre_save_receiver_tag(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, False)


class Post(models.Model):
    user_id = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True, blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='post_thumbnails', height_field=None, width_field=None, max_length=None)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    published_at = models.DateTimeField(
        blank=True, null=True, auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(
        blank=True, null=True, auto_now=False, auto_now_add=False)
    views = models.PositiveIntegerField(default=0, blank=True, null=True)
    comments = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:post_detail', kwargs={'id': self.pk, 'slug': self.slug})


@receiver(pre_save, sender=Post)
def slug_pre_save_receiver_post(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, True)


class PostTag(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_id.name

    def get_absolute_url(self):
        return reverse('post:post_tag_search', kwargs={'tag': self.tag_id.name})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment by {}'.format(self.name)
