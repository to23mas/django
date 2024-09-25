import datetime
from typing import List, Tuple
from django.http import QueryDict

from domain.data.content_progress.ContentProgressStorage import finish_project, unlock_project
from domain.data.progress.ProgressStorage import finish_chapter, finish_lesson, unlock_chapter, unlock_lesson
from domain.data.tests.QuestionData import QuestionData
from domain.data.tests.TestData import TestData
from domain.data.tests.TestResultData import TestResultData
from domain.data.tests.enum.QuestionType import QuestionType
from domain.data.tests.enum.TestState import TestState
from domain.data.tests_progress.TestProgressData import TestProgressData
from domain.data.tests_progress.TestProgressStorage import get_test_progress, reset_lock, update_test_progress

def get_test_results(user_answers: QueryDict, questionDataCollection: List[QuestionData]) -> float:
	correct_points = 0

	for question in questionDataCollection:
		if question.type == QuestionType.SINGLE.value:
			if str(user_answers.get(question.question)) in question.correct :
				correct_points += question.points

		if question.type == QuestionType.MULTIPLE.value:
			user_selected = set(user_answers.getlist(question.question)) #type: ignore
			right_answer_numbers = set(question.correct)
			wrong_answer_numbers = set(set(question.answers.keys()) ^ right_answer_numbers) #type: ignore

			rightly_selected = list(user_selected & right_answer_numbers)
			rightly_not_selected = wrong_answer_numbers - user_selected
			correct_points += (len(rightly_not_selected) + len(rightly_selected))*(question.points/len(question.answers))  #type: ignore

		if question.type == QuestionType.OPEN.value:
			processed_answer = str(user_answers.get(question.question)).lower().strip()
			processed_array = [s.lower() for s in question.correct]
			if processed_answer in processed_array:
				correct_points += question.points

	return correct_points


def validate_test_get_result(
	user_answers: QueryDict,
	test_data: TestData,
	questionDataCollection: List[QuestionData],
	course: str,
	username: str,
	test_id: int,
) -> Tuple[TestResultData, bool]:
	"""Validate test data/ users answers and return result"""

	test_result = get_test_results(user_answers, questionDataCollection)
	test_result_data = TestResultData(
		score_total=int(test_result),
		success=(test_result / test_data.total_points * 100) >= test_data.success_score,
		score_percentage=test_result / test_data.total_points * 100,
	)
	progress_happened = make_progress(test_result_data, test_data, course, username, test_id)

	return (test_result_data, progress_happened)


def make_progress(test_result_data: TestResultData, test_data: TestData, course: str, username: str, test_id: int) -> bool:
	"""Make progress if possible"""
	current_test_progress = get_test_progress(course, username, test_id)
	if current_test_progress == None or current_test_progress.attempts == 0: return False

	if test_result_data.score_percentage >= 99.99:
		new_test_state = TestState.FINISH
	elif test_result_data.score_percentage >= test_data.success_score:
		new_test_state = TestState.SUCCESS
	else:
		new_test_state = TestState.FAIL

	if new_test_state == TestState.FAIL:
		current_test_progress.attempts -= 1

	update_test_progress(course, username, test_id, test_result_data.score_total, new_test_state, current_test_progress.attempts)
	if new_test_state != TestState.FAIL:
		if (test_data.unlock_project != 0):
			unlock_project(course, username, test_data.unlock_project)
		if (test_data.unlock_lesson != 0):
			unlock_lesson(username, course, test_data.unlock_lesson)
		if (test_data.unlock_chapter != 0):
			unlock_chapter(username, course, test_data.unlock_chapter)
		if (test_data.finish_project != 0):
			finish_project(course, username, test_data.finish_project)
		if (test_data.finish_lesson != 0):
			finish_lesson(username, course, test_data.finish_lesson)
		if (test_data.finish_chapter != 0):
			finish_chapter(username, course, test_data.finish_chapter)
	return True


def reset_test_lock_time(progress:  TestProgressData, db: str, username: str, test: TestData):
	if isinstance(progress.lock_until, str): return
	current_time = datetime.datetime.now()
	time_difference = progress.lock_until - current_time
	# TODO test this
	if time_difference.total_seconds() > 15 * 60: return

	reset_lock(db, username, test.id, test.attempts)


