import datetime
from math import ceil
from django import template
from domain.data.tests_progress.TestProgressData import TestProgressData
from domain.data.tests_progress.TestProgressStorage import TestProgressStorage


register = template.Library()

@register.simple_tag
def get_test_state(course: str, username: str, test_id: int) -> TestProgressData | None:
	return TestProgressStorage().get_test_progress(course, username, test_id)

@register.simple_tag
def compare_current_timestamp(lock_until: datetime.datetime|str) -> float:
	if isinstance(lock_until, str):
		return 0.0
	current_time = datetime.datetime.now()
	time_difference = lock_until - current_time

	return ceil(time_difference.total_seconds() / 60)
