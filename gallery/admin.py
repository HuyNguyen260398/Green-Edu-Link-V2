from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    readonly_fields = ['image_load']

    def image_load(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
        ))


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ['video_load']

    def video_load(self, obj):
        return mark_safe('<iframe width="512" height="256" src="{url}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(
            url=obj.embed_url,
        ))
