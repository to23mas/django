import json
import random
from copy import deepcopy
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.domain.data.tests.enum.TestState import TestState

def generate_progress(base_data, progress_level):
    data = deepcopy(base_data)
    
    # First determine test states and scores
    test_states = {}
    for test in data["tests"]:
        test_id = test["test_id"]
        if test_id < progress_level:
            # For completed tests, randomly choose between success, finish, or fail
            state_choice = random.choices(
                [TestState.SUCCESS.value, TestState.FINISH.value, TestState.FAIL.value],
                weights=[0.4, 0.4, 0.2]  # 40% success, 40% finish, 20% fail
            )[0]
            
            # Generate multiple attempts
            attempts = random.randint(1, 5)
            scores = []
            
            if state_choice == TestState.SUCCESS.value:
                # For success, last attempt is perfect, previous attempts are lower
                for attempt in range(attempts - 1):
                    scores.append(random.randint(1, 29))  # Failed attempts
                scores.append(45)  # Perfect score on last attempt
            elif state_choice == TestState.FINISH.value:
                # For finish, last attempt is good, previous attempts are lower
                for attempt in range(attempts - 1):
                    scores.append(random.randint(1, 29))  # Failed attempts
                scores.append(random.randint(30, 44))  # Good score on last attempt
            else:  # FAIL
                # For fail, all attempts are below passing
                for attempt in range(attempts):
                    scores.append(random.randint(1, 29))  # All attempts failed
            
            test_states[test_id] = {
                "state": state_choice,
                "scores": scores,
                "attempts": attempts
            }
        elif test_id == progress_level:
            test_states[test_id] = {
                "state": TestState.OPEN.value,
                "scores": [],
                "attempts": 0
            }
        else:
            test_states[test_id] = {
                "state": TestState.CLOSE.value,
                "scores": [],
                "attempts": 0
            }

    # Find the last successful test
    last_successful_test = 0
    for test_id in sorted(test_states.keys()):
        if test_states[test_id]["state"] in [TestState.SUCCESS.value, TestState.FINISH.value]:
            last_successful_test = test_id
        else:
            break  # Stop at first failure

    # Projects progress - based on last successful test
    for i in range(1, 14):
        if i <= last_successful_test:
            data["projects"][str(i)] = "done"
        elif i == last_successful_test + 1:
            data["projects"][str(i)] = "open"
        else:
            data["projects"][str(i)] = "lock"

    # Lessons progress - based on last successful test
    for chapter in range(1, 14):
        if chapter <= last_successful_test:
            # All lessons done in completed chapters
            for lesson in range(1, 10):
                if str(lesson) in data["lessons"][str(chapter)]:
                    data["lessons"][str(chapter)][str(lesson)] = "done"
        elif chapter == last_successful_test + 1:
            # Some lessons done in current chapter
            current_lessons = list(data["lessons"][str(chapter)].keys())
            done_count = random.randint(1, len(current_lessons) - 1)
            for i, lesson in enumerate(current_lessons):
                if i < done_count:
                    data["lessons"][str(chapter)][lesson] = "done"
                elif i == done_count:
                    data["lessons"][str(chapter)][lesson] = "open"
                else:
                    data["lessons"][str(chapter)][lesson] = "lock"
        else:
            # All lessons locked in future chapters
            for lesson in data["lessons"][str(chapter)]:
                data["lessons"][str(chapter)][lesson] = "lock"

    # Chapters progress - based on last successful test
    for chapter in range(1, 14):
        if chapter <= last_successful_test:
            # All chapters done in completed chapters
            for section in data["chapters"][str(chapter)]:
                data["chapters"][str(chapter)][section] = "done"
        elif chapter == last_successful_test + 1:
            # Some sections done in current chapter
            current_sections = list(data["chapters"][str(chapter)].keys())
            done_count = random.randint(1, len(current_sections) - 1)
            for i, section in enumerate(current_sections):
                if i < done_count:
                    data["chapters"][str(chapter)][section] = "done"
                elif i == done_count:
                    data["chapters"][str(chapter)][section] = "open"
                else:
                    data["chapters"][str(chapter)][section] = "lock"
        else:
            # All sections locked in future chapters
            for section in data["chapters"][str(chapter)]:
                data["chapters"][str(chapter)][section] = "lock"

    # Update tests with the determined states
    for test in data["tests"]:
        test_id = test["test_id"]
        test_state = test_states[test_id]
        test["state"] = test_state["state"]
        test["score"] = test_state["scores"]
        test["attempts"] = test_state["attempts"]

    return data

# Load base data
with open('student.json', 'r') as f:
    base_data = json.load(f)

# Generate progress files for each student
progress_levels = [3, 5, 7, 9, 11]  # Different progress levels for each student

for i, progress_level in enumerate(progress_levels, 1):
    student_data = generate_progress(base_data, progress_level)
    student_data["_id"] = f"student_{i}"
    
    with open(f'student_{i}.json', 'w') as f:
        json.dump(student_data, f, indent=2)