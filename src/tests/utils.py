from typing import List
from django.http import QueryDict

from domain.data.content_progress.ContentProgressStorage import finish_project, unlock_project
from domain.data.tests.QuestionData import QuestionData
from domain.data.tests.TestData import TestData
from domain.data.tests.TestResultData import TestResultData
from domain.data.tests.enum.QuestionType import QuestionType
from domain.data.tests.enum.TargetUnlockType import TargetUnlockType
from domain.data.tests.enum.TestState import TestState
from domain.data.tests_progress.TestProgressStorage import update_test_progress

def get_test_results(user_answers: QueryDict, questionDataCollection: List[QuestionData]) -> float:
	correct_points = 0

	for question in questionDataCollection:
		if question.type == QuestionType.SINGLE.value:
			if question.correct == user_answers.get(question.question):
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
	test_no: str,
	) -> TestResultData:
	"""Validate test data/ users answers and return result"""

	test_result = get_test_results(user_answers, questionDataCollection)
	test_result_data = TestResultData(
		score_total=int(test_result),
		success=(test_result / test_data.total_points * 100) >= test_data.success_score,
		score_percentage=test_result / test_data.total_points * 100,
		target_unlock_type=test_data.target_type,
		target_no=test_data.target_no,
		source_no=test_data.source_no,
	)
	make_progress(test_result_data, test_data, course, username, test_no)

	return test_result_data


def make_progress(test_result_data: TestResultData, test_data: TestData, course: str, username: str, test_no: str) -> None:
	"""Make progress if possible"""

	if test_result_data.score_percentage >= 99.99:
		new_test_state = TestState.FINISH
	elif test_result_data.score_percentage >= test_data.success_score:
		new_test_state = TestState.SUCCESS
	else:
		new_test_state = TestState.FAIL

	update_test_progress(course, username, test_no, test_result_data.score_total, new_test_state)

	if not new_test_state == TestState.FAIL:
		if test_result_data.target_unlock_type == TargetUnlockType.PROJECT.value:
			unlock_project(username, test_result_data.target_no)
			finish_project(username, test_result_data.source_no)
		elif test_result_data.target_unlock_type == TargetUnlockType.LESSON.value:
			# unlock_lesson(username, course, test_result_data.target_no )
			pass
		elif test_result_data.target_unlock_type == TargetUnlockType.CHAPTER.value:
			# unlock_chapter()
			pass
	pass

