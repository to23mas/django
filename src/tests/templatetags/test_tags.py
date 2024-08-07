from django import template
from domain.data.tests_progress.TestProgressData import TestProgressData
from domain.data.tests_progress.TestProgressStorage import get_test_progress


register = template.Library()

@register.simple_tag
def get_test_state(course: str, username: str, test_id: int) -> TestProgressData | None:
	return get_test_progress(course, username, test_id)
