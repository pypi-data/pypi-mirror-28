import uuid

from django.conf import settings
from django.core.cache import cache
from django.utils import six


def get_tag_id():
    return str(uuid.uuid4())


def get_cache_key(tag_id):
    """Returns a cache key based on a tag id"""
    return 'lazy_tags_{0}'.format(tag_id)


def set_lazy_tag_data(tag_id, tag, args=None, kwargs=None):
    tag_context = {
        'tag': tag,
        'args': args,
        'kwargs': kwargs,
    }

    key = get_cache_key(tag_id)
    cache_timeout = getattr(settings, 'LAZY_TAGS_CACHE_TIMEOUT', 60)
    cache.set(key, tag_context, cache_timeout)


def get_lazy_tag_data(tag_id):
    key = get_cache_key(tag_id)
    tag_data = cache.get(key)
    cache.delete(key)
    return tag_data


def get_lib_and_tag_name(tag):
    """
    Takes a tag string and returns the tag library and tag name. For example,
    "app_tags.tag_name" is returned as "app_tags", "tag_name" and
    "app_tags.sub.tag_name" is returned as "app_tags.sub", "tag_name"
    """
    if '.' not in tag:
        raise ValueError('Tag string must be in the format "tag_lib.tag_name"')
    lib = tag.rpartition('.')[0]
    tag_name = tag.rpartition('.')[-1]
    return lib, tag_name


def get_tag_html(tag_id):
    """
    Returns the Django HTML to load the tag library and render the tag.

    Args:
        tag_id (str): The tag id for the to return the HTML for.
    """
    tag_data = get_lazy_tag_data(tag_id)
    tag = tag_data['tag']
    args = tag_data['args']
    kwargs = tag_data['kwargs']
    lib, tag_name = get_lib_and_tag_name(tag)

    args_str = ''
    if args:
        for arg in args:
            if isinstance(arg, six.string_types):
                args_str += "'{0}' ".format(arg)
            else:
                args_str += "{0} ".format(arg)

    kwargs_str = ''
    if kwargs:
        for name, value in kwargs.items():
            if isinstance(value, six.string_types):
                kwargs_str += "{0}='{1}' ".format(name, value)
            else:
                kwargs_str += "{0}={1} ".format(name, value)

    html = '{{% load {lib} %}}{{% {tag_name} {args}{kwargs}%}}'.format(
        lib=lib, tag_name=tag_name, args=args_str, kwargs=kwargs_str)

    return html
