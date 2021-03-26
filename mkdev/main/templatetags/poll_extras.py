from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def initial_letter_filter(text,):
    s = text
    return s[::-1]