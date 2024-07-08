from django.http import QueryDict

from domain.data.progress_storage import update_test_progress
from domain.data.tests_progress.test_progress_state import TestState
from domain.data.tests_progress.test_progress_storage import get_test_progress

def get_test_results(userAnswers: QueryDict, testData: dict) -> float:
    correct = 0.0

    for question in testData['questions']:
        if question['type'] == 'single':
            if question['correct'] == userAnswers.get(question['question']):
                correct += 1

        if question['type'] == 'multiple':
            correctAnswers = len(set(userAnswers.get(question['question'])).intersection(set(question['correct']))) #type: ignore
            if correctAnswers != 0:
                correct +=  correctAnswers / len(question['correct'])

        if question['type'] == 'open':
            processed_answer = str(userAnswers.get(question['question'])).lower().strip()
            processed_array = [s.lower() for s in question['correct']]

            if processed_answer in processed_array:
                correct += 1

    return (correct / len(testData['questions'])) * 100

def progress_test(userAnswers: QueryDict, testData: dict, course: str, username: str, test_no: str) -> bool:
    test_result = get_test_results(userAnswers, testData)
    user_test_progress = get_test_progress(course, username, test_no)

    # check if test is unlock and so on
    if user_test_progress == None: return False
    if (user_test_progress['state'] == TestState.FINISH.value) or (user_test_progress['state'] == TestState.CLOSE): return False

    if (test_result >= testData['success_score']):
        test_state = TestState.FINISH.value if test_result == 100 else TestState.DONE.value
        result  = True
    else:
        test_state = TestState.FAIL
        result = False

    update_test_progress(course, username, test_no, test_result, test_state)
    #TODO -> unlock? something? right?

    return result
