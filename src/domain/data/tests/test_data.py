from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class QuestionData():
    question: str
    type: str
    answers: Optional[Dict[str, str]]
    correct: Union[str, List[str]]

@dataclass
class TestData():
    no: int
    title: str
    time: int
    description: str
    target_type: str
    target_no: int
    attempts: int
    success_score: float
