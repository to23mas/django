from dataclasses import dataclass


@dataclass
class CliData():
	id: int
	title: str
	task_description: str
	expected_output: str
