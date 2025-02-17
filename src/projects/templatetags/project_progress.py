from django import template

from domain.data.progress.ProgressStorage import ProgressStorage


register = template.Library()

@register.simple_tag
def get_project_state_tag(course: str, username: str, project_id: int) -> str:
	return ProgressStorage().get_project_state(course, username, project_id)
