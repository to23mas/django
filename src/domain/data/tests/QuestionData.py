from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class QuestionData():

	id: int
	question: str
	type: str
	answers: Optional[Dict[str, str]]
	correct: List[str]
	points: int
