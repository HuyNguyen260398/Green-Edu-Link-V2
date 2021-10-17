from django.utils.text import slugify
import random
import string
import boto3


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

def get_s3_filenames():
    filenames = []
    s3 = boto3.client("s3")
    bucket = "green-edu-link-v2"
    prefix = "static/img/schools"
    result = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for item in result['Contents']:
        files = item['Key'].replace("static/", "")
        # print(files)
        filenames.append(files)
    return filenames