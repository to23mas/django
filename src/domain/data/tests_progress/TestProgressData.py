from dataclasses import dataclass
from typing import List

from domain.data.tests.enum.TestState import TestState


@dataclass
class TestProgressData():
    test_no:    int
    attempts:   int
    state:      TestState
    score:      List[int]
