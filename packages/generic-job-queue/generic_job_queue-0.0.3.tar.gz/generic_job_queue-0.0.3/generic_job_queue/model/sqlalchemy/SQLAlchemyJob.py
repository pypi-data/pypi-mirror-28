import json
import traceback
from datetime import datetime

from sqlalchemy.orm import session

from generic_job_queue.enum.job_status import JobStatus
from generic_job_queue.contracts.Job import Job
from .orm.JobORM import Job as SAJob
from .orm.JobLogORM import JobLog as SAJobLog


class SQLAlchemyJob(Job):
    def __init__(self, sa_session: session.Session, sa_job: SAJob):
        self.sa_session = sa_session
        self._sync_from_sa_job(sa_job)

    def _sync_from_sa_job(self, sa_job):
        self.sa_job = sa_job

    def push_back_to_queue(self):
        self.sa_job.status = JobStatus.PENDING
        self.sa_job.start_processing_at = None
        self.sa_job.completed_at = None
        self.sa_session.add(self.sa_job)
        self.sa_session.commit()
        self.sa_session.expire(self.sa_job)
        self._sync_from_sa_job(self.sa_job)

    def processing_start(self):
        self.sa_job.start_processing_at = datetime.now()
        self.sa_job.status = JobStatus.RUNNING
        self.sa_session.add(self.sa_job)
        self.sa_session.commit()
        self.sa_session.expire(self.sa_job)
        self._sync_from_sa_job(self.sa_job)

    def processing_finish(self, result):
        self.sa_job.start_processing_at = datetime.now()
        self.sa_job.status = JobStatus.FINISH
        self.sa_job.result = json.dumps(result)
        self.sa_session.add(self.sa_job)
        self.sa_session.commit()
        self.sa_session.expire(self.sa_job)
        self._sync_from_sa_job(self.sa_job)

    def processing_failure(self, error=None):
        self.sa_job.start_processing_at = datetime.now()
        self.sa_job.status = JobStatus.FAILURE
        self.sa_session.add(self.sa_job)
        self.sa_session.commit()
        self.sa_session.expire(self.sa_job)
        if error is None:
            self.add_log(traceback.format_exc())
        else:
            self.add_log(repr(error))
        self._sync_from_sa_job(self.sa_job)

    def get_logs(self):
        return list(map(lambda log: log.message, self.sa_job.logs))

    def add_log(self, log):
        self.sa_job.logs.append(SAJobLog(message=log))
        self.sa_session.add(self.sa_job)
        self.sa_session.commit()
        self.sa_session.expire(self.sa_job)

    def __setattr__(self, key, value):
        if hasattr(self, 'sa_job'):
            if hasattr(self.sa_job, key):
                return setattr(self.sa_job, key, value)
        return super().__setattr__(key, value)

    def __getattribute__(self, item):
        if item != 'sa_job' and hasattr(self, 'sa_job'):
            should_read_from_sa_job = hasattr(self.sa_job, item)
            if should_read_from_sa_job:
                return getattr(self.sa_job, item)
        return super().__getattribute__(item)

    @staticmethod
    def new_job(handler_name, payload, job_name=None):
        if job_name is None:
            job_name = handler_name
        job = SQLAlchemyJob(session.Session(), SAJob())
        job.job_name = job_name
        job.handler_name = handler_name
        job.payload = payload
        job.status = JobStatus.PENDING
        return job
