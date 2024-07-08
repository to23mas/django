from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class QuestionData():
    question: str
    type: str
    answers: Optional[Dict[str, str]]
    correct: Union[str, List[str]]
