import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.filter(name='color')
def bool_to_color(value):
    if value:
        return '#0000ff'
    else:
        return '#ff0000'


@register.filter(name='ttl')
def int_to_ttl(value):
    return 0 if value < 0 else value
