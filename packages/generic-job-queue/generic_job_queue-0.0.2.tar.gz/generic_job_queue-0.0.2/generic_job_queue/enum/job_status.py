from enum import Enum


class JobStatus(Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    FINISH = 'finish'
    FAILURE = 'failure'
