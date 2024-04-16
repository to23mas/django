from django import template

register = template.Library()

@register.filter(name='inlist')
def inlist(value, list):
    return value in list
