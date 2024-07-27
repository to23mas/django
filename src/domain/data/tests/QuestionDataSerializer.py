from typing import Dict, List, Optional
from domain.data.tests.QuestionData import QuestionData
from domain.data.tests.tableDefinition.TableDefinitions import TestQuestionTable


class QuestionDataSerializer:

	@staticmethod
	def to_dict(question_data: QuestionData) -> Dict[str, str | int | float | List[str] | Optional[Dict[str, str]]
]:
		return {
			'_id': question_data.id,
			'question': question_data.question,
			'type': question_data.type,
			'answers': question_data.answers,
			'correct': question_data.correct,
			'points': question_data.points,
		}

	@staticmethod
	def from_dict(question_data: dict) -> QuestionData:
		try:
			answers = question_data[TestQuestionTable.ANSWERS.value]
		except KeyError:
			answers = None

		return QuestionData(
			id=question_data[TestQuestionTable.ID.value],
			question=question_data[TestQuestionTable.QUESTION.value],
			type=question_data[TestQuestionTable.TYPE.value],
			answers=answers,
			correct=question_data[TestQuestionTable.CORRECT.value],
			points=question_data[TestQuestionTable.POINTS.value],
		)
