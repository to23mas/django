from django import template

register = template.Library()

@register.simple_tag
def get_lesson_status(lesson: dict, no: int) -> str:
	return str(lesson[str(no)])

