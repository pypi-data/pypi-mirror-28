from abc import ABC, abstractmethod
from generic_job_queue.enum.job_status import JobStatus


class JobQueue(ABC):
    def remove_finished_job(self):
        finished_jobs = self.search_job_by_status(JobStatus.FINISH)
        for finished_job in finished_jobs:
            self.remove_job(finished_job.id)

    @abstractmethod
    def remove_job(self, job_identify):
        pass

    @abstractmethod
    def search_job_by_status(self, status):
        pass

    @abstractmethod
    def get_job(self, job_identify):
        pass

    @abstractmethod
    def push_job(self, job):
        pass

    @abstractmethod
    def get_first_pending_job(self, handler_name):
        pass
