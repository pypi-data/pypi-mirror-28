import logging
from logging import Handler

from generic_job_queue.contracts.Job import Job


class JobLogger(Handler):
    def __init__(self, job: Job):
        super().__init__()
        self.job = job

    def emit(self, record):
        self.job.add_log(self.format(record))

    @staticmethod
    def createLoggerForJob(job: Job):
        logger = logging.getLogger(str(job.id))
        logger.addHandler(JobLogger(job))
        return logger
