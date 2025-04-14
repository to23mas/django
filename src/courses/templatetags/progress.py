from django import template
from domain.data.progress.ProgressStorage import ProgressStorage

register = template.Library()

@register.simple_tag
def get_course_progress(database: str, username: str) -> bool :
	progress = ProgressStorage().get_user_progress_by_course(username, database)
	match (progress):
		case None: return False
		case _: return True

@register.filter
def get_item(dictionary, key):
	return dictionary.get(key, 0)
