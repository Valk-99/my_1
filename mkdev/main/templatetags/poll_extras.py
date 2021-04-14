from django import template

register = template.Library()


@register.filter()
def initial_letter_filter(text,):
    s = text
    return s[::-1]
