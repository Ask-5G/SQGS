from django import template

register = template.Library()

@register.filter
def index(data, i):
    return data[int(i)]