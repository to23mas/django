from domain.data.tests.QuestionData import QuestionData
from domain.data.tests.tableDefinition.TableDefinitions import TestQuestionTable


class QuestionDataSerializer:

	@staticmethod
	def from_array(questionData: dict) -> QuestionData:
		try:
			answers = questionData[TestQuestionTable.ANSWERS.value]
		except KeyError:
			answers = None

		return QuestionData(
			question=questionData[TestQuestionTable.QUESTION.value],
			type=questionData[TestQuestionTable.TYPE.value],
			answers=answers,
			correct=questionData[TestQuestionTable.CORRECT.value],
			points=questionData[TestQuestionTable.POINTS.value],
		)
