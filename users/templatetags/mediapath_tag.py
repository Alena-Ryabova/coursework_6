from django import template

register = template.Library()


@register.simple_tag
def mediapath(data):
    if data:
        return f'/media/{data}'
    return '#'