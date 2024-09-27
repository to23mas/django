from django import template

from domain.data.progress.ProgressStorage import get_chapter_state, get_lesson_state

register = template.Library()

@register.simple_tag
def get_lesson_status(course_database: str, lesson_id: int, username: str) -> str:
	return get_lesson_state(course_database, username, lesson_id)

@register.simple_tag
def get_chapter_status(course_database: str, username: str, chapter_id: int) -> str:
	return get_chapter_state(course_database, username, chapter_id)
