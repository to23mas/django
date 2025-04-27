from django import template

from domain.data.lessons.LessonStorage import LessonStorage
from domain.data.projects.ProjectStorage import ProjectStorage


register = template.Library()


@register.simple_tag
def get_lesson_name(lesson_id: int, course_db: str, project_db: str) -> str:
	lesson = LessonStorage().get_lesson(lesson_id, course_db, project_db)
	match lesson:
		case None: return 'ERROR -> no lesson found'
		case _: return lesson.title

@register.simple_tag
def get_lesson_name2(lesson_id: int, course_db: str, project_id: str) -> str:
	project = ProjectStorage().get_project_by_id(int(project_id), course_db)
	if not project:
		return 'no project found'

	lesson = LessonStorage().get_lesson(int(lesson_id), course_db, project.database)

	match lesson:
		case None: return 'no name'
		case _: return lesson.title
