from enum import Enum

class ProgressState(Enum):
    OPEN = 'open'
    LOCK = 'lock'
    DONE = 'done'
