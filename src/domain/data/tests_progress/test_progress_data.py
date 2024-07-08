from dataclasses import dataclass
from typing import List

from domain.data.tests_progress.test_progress_state import TestState


@dataclass
class TestProgress():
    test_no:    int
    attempts:   int
    state:      TestState
    score:      List[int]
