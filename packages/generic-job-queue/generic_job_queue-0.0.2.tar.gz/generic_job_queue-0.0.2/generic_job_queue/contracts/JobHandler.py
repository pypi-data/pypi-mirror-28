from logging import Logger
from abc import ABC, abstractmethod

from .Job import Job


class JobHandler(ABC):
    @abstractmethod
    def handle(self, job: Job, job_logger: Logger):
        pass
