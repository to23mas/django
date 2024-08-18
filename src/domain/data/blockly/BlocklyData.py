from dataclasses import dataclass
from typing import Dict


@dataclass
class BlocklyData():
	id: int
	title: str
	toolbox: Dict
