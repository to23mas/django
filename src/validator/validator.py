from django.contrib import messages
import ast
from django.urls import reverse
from RestrictedPython.PrintCollector import PrintCollector
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

from domain.data.blockly.BlocklyStorage import BlocklyStorage
from domain.data.blockly.enum.ExpectedTaskTypes import ExpectedTaskTypes
from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.ChapterStorage import ChapterStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.ProjectStorage import ProjectStorage


# TODO add ast
FORBIDDEN_NODES = {"Import", "ImportFrom", "Exec", "Eval", "Call"}
def is_code_safe(code):
	"""
	Ověří, zda Python kód neobsahuje zakázané konstrukce.
	- Používá `ast` pro analýzu kódu místo jednoduchých regexů.
	"""
	try:
		# Převede kód na abstraktní syntaktický strom (AST)
		tree = ast.parse(code)

		for node in ast.walk(tree):
			# Kontrola, zda kód obsahuje zakázané uzly (Import, Exec, atd.)
			if type(node).__name__ in FORBIDDEN_NODES:
				print(f"❌ Zakázaná funkce: {type(node).__name__}")
				return False

			# Pokud je to volání funkce, ověříme, zda je povolená
			# if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
			# 	if node.func.id not in ALLOWED_BLOCKS:
			# 		print(f"❌ Nepovolená funkce: {node.func.id}")
			# 		return False

		return True  # ✅ Kód je bezpečný

	except SyntaxError:
		print("❌ Chyba: Kód obsahuje syntaktickou chybu!")
		return False



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

	match (blockly.expected_task):
		case ExpectedTaskTypes.PRINT.value:
			code_result = validate_python_code_print_safe(code)
			if code_result.endswith("\n"):
				code_result = code_result[:-1]
		case _:
			code_result = ''

	if blockly.expected_result == code_result:
		match (unlock_next_chapter_blockly(username, course_db, project, chapter)):
			case 'already done': return JsonResponse({'status': 'success', 'message': 'Správně'})
			case 'error': return JsonResponse({'status': 'error', 'message': 'Nevalidní akce'})
			case 'success':
				messages.success(request, 'Kapitola splněna')
				url = reverse('lessons:lesson', kwargs={
					'course': course_db,
					'project_id': project_id,
					'lesson_id': chapter.lesson_id,
					'chapter_id': chapter.id})
				return JsonResponse({'status': 'success', 'redirect': True, 'url': url})
	return JsonResponse({'status': 'error', 'message': 'Nesprávná opověď'})


def validate_python_code_print_safe(code):
	print_result = 'printed_result_validation_string_collection_grabber'
	code += f'\n{print_result} = printed'
	restricted_locals = {}
	restricted_globals = {
		"__builtins__": safe_builtins,
		"_print_": PrintCollector,
		"_getattr_":  getattr,
	}

	byte_code = compile_restricted(code, '<string>', 'exec')
	exec(byte_code, restricted_globals, restricted_locals) #pylint: disable=W0122
	output = restricted_locals[print_result]

	return output

def unlock_next_chapter_blockly(username: str, course_db: str, project: ProjectData, chapter: ChapterData) -> str:
	if chapter.unlock_type != 'blockly':
		return 'error'

	if not ProgressStorage().is_chapter_open(username, course_db, project.id, chapter.lesson_id, chapter.id): #type: ignore
		if (ProgressStorage().is_chapter_done(username, course_db, chapter.id)):
			return 'already done'

		return 'error'

	next_chapter = ChapterStorage().get_chapter_by_id(chapter.unlock_id, course_db, project.database)
	if next_chapter is not None:
		ProgressStorage().unlock_lesson(username, course_db, next_chapter.lesson_id)
		ProgressStorage().unlock_chapter(username, course_db, next_chapter.id)

	ProgressStorage().finish_chapter(username, course_db, chapter.id)

	if chapter.is_last_in_lesson:
		ProgressStorage().finish_lesson(username, course_db, chapter.lesson_id)

	if next_chapter is None:
		#last chapter in project
		# finish_project()
		# unlock_project()
		## probably unlock next project
		return 'success'

	return 'success'

