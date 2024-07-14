from django import template

from domain.data.lessons.LessonStorage import get_lesson
from domain.data.projects.ProjectStorage import get_project


register = template.Library()

@register.filter("get_project_name_from_id")
def get_project_name_from_id(project_no: str, course: str):
	project, _ = get_project(int(project_no), course)

	return project.title #type: ignore


@register.simple_tag
def get_lesson_name_from_id(lesson_no: str, project_no: str, course: str) -> str:
	lesson = get_lesson(lesson_no, project_no, course )
	return lesson.title #type: ignore
