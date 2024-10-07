from django import template

register = template.Library()

@register.filter(name='inlist')
def inlist(value, list_):
	return value in list_
