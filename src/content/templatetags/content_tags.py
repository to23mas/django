from django import template

from domain.data.lessons.LessonStorage import get_lesson
from domain.data.projects.ProjectStorage import get_project


register = template.Library()

@register.filter("get_project_name_from_id")
def get_project_name_from_id(project_no: str, course: str):
	project, _ = get_project(int(project_no), course)

	return project.title #type: ignore


@register.simple_tag
def get_lesson_name(lesson_id: int, course_db: str, project_db: str) -> str:
	lesson = get_lesson(lesson_id, course_db, project_db)
	print(lesson)
	match lesson:
		case None: return 'ERROR -> no lesson found'
		case _: return lesson.title
