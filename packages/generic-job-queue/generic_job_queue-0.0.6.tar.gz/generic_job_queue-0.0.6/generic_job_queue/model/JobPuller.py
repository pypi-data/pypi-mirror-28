import time
import logging

from typing import Dict

from generic_job_queue.contracts.Job import Job
from generic_job_queue.contracts.JobHandler import JobHandler
from generic_job_queue.model.sqlalchemy.SQLAlchemyJobQueue import SQLAlchemyJobQueue
from .JobLogger import JobLogger

logger = logging.getLogger(__name__)

class JobPuller:
    def __init__(self, sa_session_maker):
        self.sa_session_maker = sa_session_maker
        self._handlers: Dict[str, JobHandler] = {}
        self.running = False

    def set_handler(self, handler_name, handler: JobHandler):
        self._handlers[handler_name] = handler

    def unset_handler(self, handler_name):
        del self._handlers[handler_name]

    def start(self):
        self.running = True
        while self.running:
            has_any_job = False
            for handler_name, handler in self._handlers.items():
                session = self.sa_session_maker()
                try:
                    job = self._pull_job(session, handler_name)
                    has_job = job is not None
                    if has_job:
                        has_any_job = True
                        self._execute_job(job, handler)
                    session.commit()
                except Exception as e:
                    logger.error(e, exc_info=True)
                    session.rollback()
                finally:
                    session.close()
            if not has_any_job:
                time.sleep(60)

    def _pull_job(self, session, handler_name) -> Job:
        queue = SQLAlchemyJobQueue(
            session
        )
        return queue.get_first_pending_job(handler_name)

    def _execute_job(self, job, job_handler):
        try:
            job.processing_start()
            job_logger = JobLogger.createLoggerForJob(job)
            job_result = job_handler.handle(job, job_logger)
            job.processing_finish(job_result)
        except Exception as e:
            job.processing_failure(e)

    def stop(self):
        self.running = False
