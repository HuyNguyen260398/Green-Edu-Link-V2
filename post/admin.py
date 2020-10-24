from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Post,
    Category,
    Tag,
    PostTag,
    Comment,
)


class PostTagInline(admin.TabularInline):
    model = PostTag
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    readonly_fields = ['thumbnail_load']
    fields = (
        'user_id',
        'category',
        'sub_category',
        'title',
        'description',
        'slug',
        'thumbnail',
        'thumbnail_load',
        'content',
        'published_at',
        'updated_at',
        'views',
        'comments',
    )
    inlines = [PostTagInline]

    def thumbnail_load(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.thumbnail.url,
            width=obj.thumbnail.width,
            height=obj.thumbnail.height,
        ))

    class Meta:
        model = Post


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'create_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comment(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Post, PostAdmin)

admin.site.register(Category)

admin.site.register(Tag)

admin.site.register(PostTag)

admin.site.register(Comment)
