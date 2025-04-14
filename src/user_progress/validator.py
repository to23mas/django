import os
import docker
from django.conf import settings
import ast

from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from domain.data.blockly.BlocklyStorage import BlocklyStorage
from domain.data.blockly.enum.ExpectedTaskTypes import ExpectedTaskTypes
from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.ChapterStorage import ChapterStorage

from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.ProjectStorage import ProjectStorage

from .validators.print_validator import validate_python_code_print
from .validators.function_validator import validate_python_code_function
from .validators.variable_validator import validate_python_code_variable
from .validators.variable_pattern_validator import validate_variable_pattern


@login_required
def validate_python(request: HttpRequest) -> HttpResponse:
	"""list all projects"""

	username = request.user.username #type: ignore
	code = str(request.POST.get('code', ''))
	blockly_id = str(request.POST.get('blockly_id', ''))
	course_db = str(request.POST.get('course_db', ''))
	chapter_id = int(str(request.POST.get('chapter_id')))
	lesson_id = int(str(request.POST.get('lesson_id')))
	project_id = int(str(request.POST.get('project_id')))

	project = ProjectStorage().get_project_by_id(project_id, course_db)
	if project is None:
		return JsonResponse({'status': 'error', 'message': 'Nevalidní akce'})
	chapter = ChapterStorage().get_chapter(chapter_id, lesson_id, course_db, project.database)
	if chapter is None:
		return JsonResponse({'status': 'error', 'message': 'Nevalidní akce'})
	blockly = BlocklyStorage().get_blockly(course_db, int(blockly_id))
	if blockly is None:
		return JsonResponse({'status': 'error', 'message': 'Nevalidní akce'})

	if not check_ast(code):
		return JsonResponse({
			'status': 'error',
			'message': 'Kód nebylo možné spustit, obsahuje nebezpečné konstrukty.'
		})

	code_result = validate_task(blockly.expected_task, code, username, blockly.expected_result)

	if code_result == True:
		return handle_success(username, course_db, project, chapter)

	return JsonResponse({'status': 'error', 'message': 'Nesprávná odpověď'})


def check_ast(code: str) -> bool:
	try:
		tree = ast.parse(code)

		for node in ast.walk(tree):
			# Check for imports
			if isinstance(node, (ast.Import, ast.ImportFrom)):
				return False

			# Check for system/file operations
			if isinstance(node, ast.Call):
				if isinstance(node.func, ast.Name):
					# Dangerous built-in functions
					dangerous_functions = {
						'eval', 'exec', 'open', 'compile',
						'input', '__import__', 'getattr', 'setattr',
						'globals', 'locals', 'vars'
					}
					if node.func.id in dangerous_functions:
						return False

			# Check for attribute access
			if isinstance(node, ast.Attribute):
				# Dangerous attributes/methods
				dangerous_attrs = {
					'read', 'write', 'system', 'popen',
					'subprocess', 'shell', 'eval', 'exec'
				}
				if node.attr in dangerous_attrs:
					return False

		return True

	except SyntaxError:
		return False


def validate_task(task_type: str, code: str, username: str, expected_result: str) -> bool:
	match task_type:
		case ExpectedTaskTypes.PRINT.value:
			result = validate_python_code_print(code, username)
			if result.endswith("\n"):
				result = result[:-1]
			return result == expected_result

		case ExpectedTaskTypes.FUNCTION.value:
			result = validate_python_code_function(code, username, expected_result)
			if result.endswith("\n"):
				result = result[:-1]
			return result.strip() == 'True'

		case ExpectedTaskTypes.VARIABLE.value:
			return validate_python_code_variable(code, username, expected_result)

		case ExpectedTaskTypes.VARIABLE_PATTERN.value:
			return validate_variable_pattern(code, username, expected_result)

		case _:
			return False


def handle_success(username: str, course_db: str, project: ProjectData, chapter: ChapterData) -> JsonResponse:
	match unlock_next_chapter_blockly(username, course_db, project, chapter):
		case 'already done':
			return JsonResponse({'status': 'success', 'message': 'Správně'})
		case 'error':
			return JsonResponse({'status': 'error', 'message': 'Nevalidní akce'})
		case 'success':
			next_chapter_data = ChapterStorage().get_chapter_by_id(chapter.unlock_id, course_db, project.database)
			if next_chapter_data is None:
				url = reverse('projects:overview', course=course_db, sort_type='all')
			else:
				url = reverse('lessons:lesson', kwargs={
					'course': course_db,
					'project_id': project.id,
					'lesson_id': next_chapter_data.lesson_id,
					'chapter_id': next_chapter_data.id
				})

			return JsonResponse({
				'status': 'success',
				'redirect': True,
				'url': url
			})


def unlock_next_chapter_blockly(username: str, course_db: str, project: ProjectData, chapter: ChapterData) -> str:
	if chapter.unlock_type != 'blockly':
		return 'error'

	if not ProgressStorage().is_chapter_open(username, course_db, project.id, chapter.lesson_id, chapter.id): #type: ignore
		if (ProgressStorage().is_chapter_done(username, course_db, chapter.id, project.id)):
			return 'already done'

		return 'error'

	next_chapter = ChapterStorage().get_chapter_by_id(chapter.unlock_id, course_db, project.database)
	if next_chapter is not None:
		ProgressStorage().unlock_lesson(username, course_db, next_chapter.lesson_id, project.id)
		ProgressStorage().unlock_chapter(username, course_db, next_chapter.id, project.id)

	ProgressStorage().finish_chapter(username, course_db, chapter.id, project.id)

	if chapter.is_last_in_lesson:
		ProgressStorage().finish_lesson(username, course_db, chapter.lesson_id, project.id)

	if next_chapter is None:
		#last chapter in project
		# finish_project()
		# unlock_project()
		## probably unlock next project
		return 'success'

	return 'success'
