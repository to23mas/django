from dataclasses import dataclass
from typing import Dict


@dataclass
class BlocklyData():
	id: int
	title: str
	task_description: str
	expected_task: str
	expected_result: str
	toolbox: Dict
