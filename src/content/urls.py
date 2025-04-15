from django.urls import path

from .views import * #pylint: disable=W0401, W0614


urlpatterns = [
	path('', course_overview, name='admin_course_overview'),
	path('users_progress', admin_users_overview, name='admin_users_overview'),
	path('users_progress/<str:username>', admin_user_progress_detail, name='admin_user_progress_detail'),
    path('users_progress/<str:username>/<str:course>', admin_user_progress_course_detail, name='admin_user_progress_course_detail'),
    path('course_progress', course_progress_overview, name='course_progress_overview'),
    path('course_progress/<str:course_id>', course_progress_detail, name='course_progress_detail'),
    path('course_progress/<str:course_id>/test/<str:test_id>/results', test_results_detail, name='test_results_detail'),

	path('course/<str:course_id>/edit', course_edit, name='admin_course_edit'),
	path('course/<str:course_id>/delete', course_delete, name='admin_course_delete'),
	path('course/<str:course_id>/download', course_download, name='admin_course_download'),
	path('course/download/user', progress_download, name='progress_download'),
	path('course/new', course_new, name='admin_course_new'),

	path('course/<str:course_id>/projects', project_overview, name='admin_project_overview'),
	path('course/<str:course_id>/projects/<int:project_id>/edit', project_edit, name='admin_project_edit'),
	path('course/<str:course_id>/projects/new', project_new, name='admin_project_new'),
	path('course/<str:course_id>/projects/<str:project_id>/delete', project_delete, name='admin_project_delete'),

	path('course/<str:course_id>-<int:project_id>/lessons', lesson_overview, name='admin_lesson_overview'),
	path('course/<str:course_id>-<int:project_id>/lessons/new', lesson_new, name='admin_lesson_new'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>/lessons/edit', lesson_edit, name='admin_lesson_edit'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>/lessons/delete', lesson_delete, name='admin_lesson_delete'),

	path('course/<str:course_id>-<int:project_id>/chapters', chapter_overview, name='admin_chapter_overview'),
	path('course/<str:course_id>-<int:project_id>/chapters/new', chapter_new, name='admin_chapter_new'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>-<int:chapter_id>/chapters/edit', chapter_edit, name='admin_chapter_edit'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>-<int:chapter_id>/chapters/delete', chapter_delete, name='admin_chapter_delete'),

	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>-<int:chapter_id>/block/new', block_new, name='admin_block_new'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>-<int:chapter_id>-<int:block_id>/block/edit', block_edit, name='admin_block_edit'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>-<int:chapter_id>-<int:block_id>/block/delete', block_delete, name='admin_block_delete'),

	path('course/<str:course_id>/tests', test_overview, name='admin_test_overview'),
	path('course/<str:course_id>/tests/new', test_new, name='admin_test_new'),
	path('course/<str:course_id>-<int:test_id>/test/edit', test_edit, name='admin_test_edit'),
	path('course/<str:course_id>-<int:test_id>/test/delete', test_delete, name='admin_test_delete'),

	path('course/<str:course_id>/blockly', blockly_overview, name='admin_blockly_overview'),
	path('course/<str:course_id>/blockly/new', blockly_new, name='admin_blockly_new'),
	path('course/<str:course_id>-<int:blockly_id>/blockly/edit', blockly_edit, name='admin_blockly_edit'),
	path('course/<str:course_id>-<int:blockly_id>/blockly/delete', blockly_delete, name='admin_blockly_delete'),

	path('course/<str:course_id>/demo', demo_overview, name='admin_demo_overview'),
	path('course/<str:course_id>/demo/new', demo_new, name='admin_demo_new'),
	path('course/<str:course_id>-<int:demo_id>/demo/edit', demo_edit, name='admin_demo_edit'),
	path('course/<str:course_id>-<int:demo_id>/demo/delete', demo_delete, name='admin_demo_delete'),

	path('course/<str:course_id>-<int:test_id>/test/new-question', test_new_question, name='admin_test_new_question'),
	path('course/<str:course_id>-<int:test_id>-<int:question_id>/test/delete-question', test_delete_question, name='admin_test_delete_question'),
	path('course/<str:course_id>-<int:test_id>-<int:question_id>/test/edit-question', test_edit_question, name='admin_test_edit_question'),

	path('course/<int:course_id>/cli/', cli_overview, name='admin_cli_overview'),
	path('course/<int:course_id>/cli/new/', cli_new, name='admin_cli_new'),
	path('course/<int:course_id>/cli/<int:cli_id>/edit/', cli_edit, name='admin_cli_edit'),
	path('course/<int:course_id>/cli/<int:cli_id>/delete/', cli_delete, name='admin_cli_delete'),
]
