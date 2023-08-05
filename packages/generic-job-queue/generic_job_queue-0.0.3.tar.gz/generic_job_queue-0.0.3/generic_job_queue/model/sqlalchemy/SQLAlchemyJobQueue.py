from sqlalchemy.orm import exc, session

from generic_job_queue.enum.job_status import JobStatus
from generic_job_queue.contracts.JobQueue import JobQueue
from .orm.JobORM import Job
from .errors import RecordNotFoundError
from .SQLAlchemyJob import SQLAlchemyJob


class SQLAlchemyJobQueue(JobQueue):
    def __init__(self, sa_session_maker):
        self.sa_session_maker = sa_session_maker

    def remove_job(self, job_identify):
        sa_session: session.Session = self.sa_session_maker()
        sa_job = sa_session.query(Job)\
            .filter(Job.id == job_identify)\
            .one_or_none()
        job_is_found = sa_job is not None
        if job_is_found:
            sa_session.delete(sa_job)
            sa_session.commit()

    def search_job_by_status(self, status):
        sa_session: session.Session = self.sa_session_maker()
        sa_jobs = sa_session \
            .query(Job) \
            .filter(Job.status == status) \
            .order_by(Job.created_at) \
            .all()
        return [SQLAlchemyJob(sa_session, sa_job) for sa_job in sa_jobs]

    def get_job(self, job_identify):
        sa_session: session.Session = self.sa_session_maker()
        try:
            sa_job = sa_session.query(Job)\
            .filter(Job.id == job_identify)\
            .one()
            return SQLAlchemyJob(sa_session, sa_job)
        except exc.NoResultFound as e:
            raise RecordNotFoundError(e)


    def push_job(self, job: SQLAlchemyJob):
        sa_session: session.Session = self.sa_session_maker()
        sa_session.add(job.sa_job)
        sa_session.commit()
        sa_session.expire(job.sa_job)
        return SQLAlchemyJob(sa_session, job.sa_job)

    def get_first_pending_job(self, handler_name):
        sa_session: session.Session = self.sa_session_maker()
        sa_job = sa_session\
            .query(Job)\
            .filter(Job.status == JobStatus.PENDING, Job.handler_name == handler_name)\
            .order_by(Job.created_at)\
            .first()
        if sa_job is not None:
            return SQLAlchemyJob(sa_session, sa_job)
        return None
