import datetime
from typing import List, Tuple
from django.http import QueryDict
from .models import TestResult

from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.tests.QuestionData import QuestionData
from domain.data.tests.TestData import TestData
from domain.data.tests.TestResultData import TestResultData
from domain.data.tests.enum.QuestionType import QuestionType
from domain.data.tests.enum.TestState import TestState
from domain.data.tests_progress.TestProgressData import TestProgressData
from domain.data.tests_progress.TestProgressStorage import TestProgressStorage
from domain.data.tests.TestStorage import TestStorage

def get_test_results(user_answers: QueryDict, questionDataCollection: List[QuestionData], test_id: int, username: str) -> float:
	correct_points = 0
	
	# Get the current attempt number for this user and test
	last_attempt = TestResult.objects.filter(user_id=username, test_id=test_id).order_by('-attempt_number').first()
	current_attempt = (last_attempt.attempt_number + 1) if last_attempt else 1

	for question in questionDataCollection:
		is_correct = False
		is_partially_correct = False
		points_earned = 0
		selected_answers = []

		if question.type == QuestionType.SINGLE.value:
			selected_answer = str(user_answers.get(question.question))
			selected_answers = [selected_answer]
			if selected_answer in question.correct:
				is_correct = True
				points_earned = question.points
				correct_points += question.points

		elif question.type == QuestionType.MULTIPLE.value:
			user_selected = set(user_answers.getlist(question.question)) #type: ignore
			selected_answers = list(user_selected)
			right_answer_numbers = set(question.correct)
			wrong_answer_numbers = set(set(question.answers.keys()) ^ right_answer_numbers) #type: ignore

			rightly_selected = list(user_selected & right_answer_numbers)
			rightly_not_selected = wrong_answer_numbers - user_selected
			points_earned = (len(rightly_not_selected) + len(rightly_selected))*(question.points/len(question.answers))  #type: ignore
			correct_points += points_earned
			is_correct = points_earned == question.points
			# Set partially correct if some but not all correct answers were selected
			is_partially_correct = True if points_earned != 0 and points_earned != question.points else False

		elif question.type == QuestionType.OPEN.value:
			processed_answer = str(user_answers.get(question.question)).lower().strip()
			selected_answers = [processed_answer]
			processed_array = [s.lower() for s in question.correct]
			if processed_answer in processed_array:
				is_correct = True
				points_earned = question.points
				correct_points += question.points

		TestResult.objects.create(
			user_id=username,
			test_id=test_id,
			question_id=question.id,
			question_type=question.type,
			selected_answers=selected_answers,
			correct_answers=question.correct,
			is_correct=is_correct,
			is_partially_correct=is_partially_correct,
			points_earned=points_earned,
			attempt_number=current_attempt,
			submitted=True
		)

	return correct_points


def fail_test(test_data: TestData, course: str, username: str, test_id: int):
	# Get the current attempt number for this user and test
	last_attempt = TestResult.objects.filter(user_id=username, test_id=test_id).order_by('-attempt_number').first()
	current_attempt = (last_attempt.attempt_number + 1) if last_attempt else 1

	# Get the questions for this test
	_, questionDataCollection = TestStorage().get_test(course, test_id)
	if questionDataCollection is None:
		return (TestResultData(score_total=0, success=False, score_percentage=0), False)

	# Create TestResult records for each question with 0 points
	for question in questionDataCollection:
		TestResult.objects.create(
			user_id=username,
			test_id=test_id,
			question_id=question.id,
			question_type=question.type,
			selected_answers=[],
			correct_answers=question.correct,
			is_correct=False,
			points_earned=0,
			attempt_number=current_attempt,
			submitted=False
		)

	test_result_data = TestResultData(
		score_total=0,
		success=False,
		score_percentage=0,
	)
	progress_happened = make_progress(test_result_data, test_data, course, username, test_id)

	return (test_result_data, progress_happened)

def validate_test_get_result(
	user_answers: QueryDict,
	test_data: TestData,
	questionDataCollection: List[QuestionData],
	course: str,
	username: str,
	test_id: int,
) -> Tuple[TestResultData, bool]:
	"""Validate test data/ users answers and return result"""

	test_result = get_test_results(user_answers, questionDataCollection, test_id, username)
	test_result_data = TestResultData(
		score_total=int(test_result),
		success=(test_result / test_data.total_points * 100) >= test_data.success_score,
		score_percentage=test_result / test_data.total_points * 100,
	)
	progress_happened = make_progress(test_result_data, test_data, course, username, test_id)

	return (test_result_data, progress_happened)


def make_progress(test_result_data: TestResultData, test_data: TestData, course: str, username: str, test_id: int) -> bool:
	"""Make progress if possible"""
	current_test_progress = TestProgressStorage().get_test_progress(course, username, test_id)
	if current_test_progress is None or current_test_progress.attempts == 0: return False

	if test_result_data.score_percentage >= 99.99:
		new_test_state = TestState.FINISH
	elif test_result_data.score_percentage >= test_data.success_score:
		new_test_state = TestState.SUCCESS
	else:
		new_test_state = TestState.FAIL

	if new_test_state in [TestState.FAIL, TestState.SUCCESS]:
		current_test_progress.attempts -= 1

	if current_test_progress.state == TestState.SUCCESS.value:
		if new_test_state != TestState.FINISH:
			new_test_state = TestState.SUCCESS

	TestProgressStorage().update_test_progress(course, username, test_id, test_result_data.score_total, new_test_state, current_test_progress.attempts)
	if new_test_state != TestState.FAIL:
		# unlock new project
		if (test_data.unlock_project != 0):
			ProgressStorage().unlock_project(course, username, test_data.unlock_project)
			ProgressStorage().unlock_lesson(username, course, test_data.unlock_lesson, test_data.unlock_project)
			ProgressStorage().unlock_chapter(username, course, test_data.unlock_chapter, test_data.unlock_project)
		else:
			#unlock inside current
			if (test_data.unlock_lesson != 0):
				ProgressStorage().unlock_lesson(username, course, test_data.unlock_lesson, test_data.current_project)
			if (test_data.unlock_chapter != 0):
				ProgressStorage().unlock_chapter(username, course, test_data.unlock_chapter, test_data.current_project)

		if (test_data.finish_project != 0):
			ProgressStorage().finish_project(course, username, test_data.finish_project)
		if (test_data.finish_lesson != 0):
			ProgressStorage().finish_lesson(username, course, test_data.finish_lesson, test_data.current_project)
		if (test_data.finish_chapter != 0):
			ProgressStorage().finish_chapter(username, course, test_data.finish_chapter, test_data.current_project)
	return True


def reset_test_lock_time(progress:  TestProgressData, db: str, username: str, test: TestData):
	if isinstance(progress.lock_until, str): return
	if (progress.lock_until > datetime.datetime.now()): return

	TestProgressStorage().reset_lock(db, username, test.id, test.attempts)

