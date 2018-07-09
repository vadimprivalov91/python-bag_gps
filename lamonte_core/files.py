from django.template.defaultfilters import slugify
from os.path import splitext


def slugify_filename(filename):
    name, ext = splitext(filename)
    slug = slugify(name)
    return slug + ext
