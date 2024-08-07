from django import template

from domain.data.content_progress.ContentProgressStorage import get_lesson_state

register = template.Library()

@register.simple_tag
def get_lesson_status(course_database: str, lesson_id: int, username: str) -> str:
	return get_lesson_state(course_database, username, lesson_id)

