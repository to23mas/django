from django import template
from domain.data.progress.ProgressStorage import get_user_progress_by_course

register = template.Library()

@register.simple_tag
def get_course_progress(database: str, username: str) -> bool :
	progress = get_user_progress_by_course(username, database)
	match (progress):
		case None: return False
		case _: return True
