from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from domain.data.clis.CliStorage import CliStorage
from domain.data.chapters.ChapterStorage import ChapterStorage
from domain.data.projects.ProjectStorage import ProjectStorage
from domain.data.progress.ProgressStorage import ProgressStorage

@login_required
def validate_cli(request: HttpRequest) -> JsonResponse:
	"""Validate CLI task answer"""
	if request.method != 'POST':
		return JsonResponse({'status': 'error', 'message': 'Nevalidní akce'})

	try:
		username = request.user.username  # type: ignore
		answer = str(request.POST.get('answer', ''))
		chapter_id = int(str(request.POST.get('chapter_id')))
		lesson_id = int(str(request.POST.get('lesson_id')))
		project_id = int(str(request.POST.get('project_id')))
		course_db = str(request.POST.get('course_db', ''))

		# Get necessary data
		project = ProjectStorage().get_project_by_id(project_id, course_db)
		if project is None:
			return JsonResponse({'status': 'error', 'message': 'Nevalidní akce'})

		chapter = ChapterStorage().get_chapter(chapter_id, lesson_id, course_db, project.database)
		if chapter is None or chapter.unlock_type != 'cli':
			return JsonResponse({'status': 'error', 'message': 'Nevalidní akce'})

		cli = CliStorage().get_cli(course_db, chapter.unlocker_id) #type: ignore
		if cli is None:
			return JsonResponse({'status': 'error', 'message': 'Nevalidní akce'})

		# Validate answer
		if cli.expected_output.strip() == answer.strip():
			# Handle successful completion
			next_chapter = ChapterStorage().get_chapter_by_id(chapter.unlock_id, course_db, project.database)
			if next_chapter is not None:
				ProgressStorage().unlock_lesson(username, course_db, next_chapter.lesson_id, project_id)
				ProgressStorage().unlock_chapter(username, course_db, next_chapter.id, project_id)

			ProgressStorage().finish_chapter(username, course_db, chapter.id, project_id)

			if chapter.is_last_in_lesson:
				ProgressStorage().finish_lesson(username, course_db, chapter.lesson_id, project_id)

			if next_chapter is None:
				url = reverse('projects:overview', course=course_db, sort_type='all')
			else: 
				url = reverse('lessons:lesson', kwargs={
					'course': course_db,
					'project_id': project_id,
					'lesson_id': next_chapter.lesson_id,
					'chapter_id': next_chapter.id
				})
			return JsonResponse({
				'status': 'success',
				'redirect': True,
				'url': url
			})

		return JsonResponse({'status': 'error', 'message': 'Nesprávná odpověď'})

	except Exception:
		return JsonResponse({'status': 'error', 'message': 'Došlo k chybě na straně serveru, opakujte akci později.'})
