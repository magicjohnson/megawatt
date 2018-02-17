from django import template
from django.urls import NoReverseMatch
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def active_url(context, urls):
    path = context['request'].path
    for url in urls.split(','):
        try:
            if reverse(url) == path:
                return "active"
        except NoReverseMatch:
            if url in path:
                return "active"

    return ''
