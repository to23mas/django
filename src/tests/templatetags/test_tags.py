from django import template
from domain.data.tests_progress.test_progress_data import TestProgress
from domain.data.tests_progress.test_progress_storage import get_test_progress


register = template.Library()

@register.simple_tag
def get_test_state(course: str, username: str, test_no: str) -> TestProgress | None:
    return get_test_progress(course, username, test_no)
