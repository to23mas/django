from django import template


register = template.Library()

@register.filter("get_type")
def get_type(value):
	return type(value)
