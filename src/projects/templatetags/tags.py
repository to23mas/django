from django import template

register = template.Library()

@register.simple_tag
def get_status(content: dict, no: int) -> str:
	return str(content[str(no)])

