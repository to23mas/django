import time
import json
import os
import docker
from django.contrib import messages
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
			code_result = validate_python_code_print_safe(code, username)
			if code_result == False:
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


def validate_python_code_print_safe(code, username: str) -> str:
	file_path = os.path.join("/tmp/", f'{username}.py')
	with open(file_path, "w") as file:
		file.write(code)

	client = docker.from_env()

	container = client.containers.run(
		image="restricted_python",
		# TODO fix for server path
		volumes={f'/home/soleus/Documents/School/master/django/tmp/{username}.py': {"bind": f"/sandbox/file.py", "mode": "ro"}},
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
	except:
		container.kill()
		raise Exception('container took too long')

	return logs[0]

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
