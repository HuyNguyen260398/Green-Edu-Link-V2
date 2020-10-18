from django.utils.text import slugify
import random
import string
import threading


def random_string_generator(
    size=10,
    chars=string.ascii_lowercase + string.digits
):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, is_post_instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        if is_post_instance:
            slug = slugify(instance.title)
        else:
            slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
