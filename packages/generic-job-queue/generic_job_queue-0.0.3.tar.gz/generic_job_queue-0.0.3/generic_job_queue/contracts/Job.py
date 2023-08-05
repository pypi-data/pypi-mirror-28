from abc import ABC, abstractmethod

class Job(ABC):
    id = None
    job_name = None
    handler_name = None
    start_processing_at = None
    completed_at = None
    payload = None
    status = None
    job_meta = None

    @abstractmethod
    def push_back_to_queue(self):
        pass

    @abstractmethod
    def processing_start(self):
        pass

    @abstractmethod
    def processing_finish(self, result):
        pass

    @abstractmethod
    def processing_failure(self, error=None):
        pass

    @abstractmethod
    def get_logs(self):
        pass

    @abstractmethod
    def add_log(self, log):
        pass
