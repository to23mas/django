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

	match (blockly.expected_task):
		case ExpectedTaskTypes.PRINT.value:
			code_result = validate_python_code_print_safe(code, username)
			if code_result.endswith("\n"):
				code_result = code_result[:-1]
				if blockly.expected_result == code_result:
					code_result = True
		case ExpectedTaskTypes.FUNCTION.value:
			code_result = validate_python_code_function_safe(code, username, blockly.expected_result)
			if code_result.endswith("\n"):
				code_result = code_result[:-1]
			code_result = (code_result.strip() == 'True')
		case _:	
			code_result = ''

	if code_result == True:
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


def validate_python_code_print_safe(code, username: str) -> str:
	os.makedirs('./tmp', exist_ok=True)
	os.chmod('./tmp', 0o777)

	file_path = os.path.join('./tmp', f'{username}.py')
	with open(file_path, "w", encoding='utf-8') as file:
		file.write(code)
	os.chmod(file_path, 0o777)

	client = docker.from_env()

	container = client.containers.run(
		image="restricted_python",
		volumes={f'{settings.VALIDATOR_DIR}/{username}.py': {"bind": "/sandbox/file.py", "mode": "ro"}},
		stdout=True,
		stderr=True,
		remove=True,  # Automatically remove container after execution
		detach=True,  # Run synchronously
		command="python /sandbox/run_code.py",  # Command to execute inside container
		cpu_count=1,  # Omezení na 1 CPU jádro
		cpu_shares=512,  # Určuje relativní prioritu (512 znamená průměrnou prioritu)
		mem_limit="128m",  # Omezení na 128 MB RAM
		memswap_limit="256m"  # Omezení na 256 MB (RAM + swap)
	)

	try:
		container.wait(timeout=10)
		logs = []
		for log in container.logs(stream=True):
			logs.append(log.decode('utf-8'))
	except Exception:
		container.kill()
		raise Exception('Container took too long')
	finally:
		if os.path.exists(file_path):
			os.remove(file_path)

	return logs[0]

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

def validate_python_code_function_safe(code: str, username: str, expected_result: str) -> str:
	lines = expected_result.strip().split('\n')
	function_name = lines[0].strip()  # First line is function name
	
	test_cases = []
	for line in lines[1:]:
		if ':' in line:
			params, expected = line.split(':')
			params = [int(p.strip()) for p in params.split(',')]
			expected = int(expected.strip().rstrip(';'))
			test_cases.append((params, expected))

	test_code = code + "\n\n# Test cases\n"
	test_code += "test_results = True\n"
	for params, expected in test_cases:
		params_str = ", ".join(str(p) for p in params)
		test_code += f"test_results = test_results and {function_name}({params_str}) == {expected}\n"
	
	test_code += "print(test_results)"
	
	os.makedirs('./tmp', exist_ok=True)
	os.chmod('./tmp', 0o777)

	file_path = os.path.join('./tmp', f'{username}.py')
	with open(file_path, "w", encoding='utf-8') as file:
		file.write(test_code)
	os.chmod(file_path, 0o777)

	client = docker.from_env()

	container = client.containers.run(
		image="restricted_python",
		volumes={f'{settings.VALIDATOR_DIR}/{username}.py': {"bind": "/sandbox/file.py", "mode": "ro"}},
		stdout=True,
		stderr=True,
		remove=True,  # Automatically remove container after execution
		detach=True,  # Run synchronously
		command="python /sandbox/run_code.py",  # Command to execute inside container
		cpu_count=1,  # Omezení na 1 CPU jádro
		cpu_shares=512,  # Určuje relativní prioritu (512 znamená průměrnou prioritu)
		mem_limit="128m",  # Omezení na 128 MB RAM
		memswap_limit="256m"  # Omezení na 256 MB (RAM + swap)
	)

	try:
		container.wait(timeout=10)
		logs = []
		for log in container.logs(stream=True):
			logs.append(log.decode('utf-8'))
	except Exception:
		container.kill()
		raise Exception('Container took too long')
	finally:
		if os.path.exists(file_path):
			os.remove(file_path)

	# Clean up the result by removing whitespace and newlines
	result = logs[0].strip()
	return result

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
