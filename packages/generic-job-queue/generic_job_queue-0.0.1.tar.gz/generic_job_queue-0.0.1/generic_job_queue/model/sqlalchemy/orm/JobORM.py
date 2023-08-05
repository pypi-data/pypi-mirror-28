from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.orm import relationship

from generic_job_queue.enum.job_status import JobStatus
from .ORMBase import Base
from .JobLogORM import JobLog


class Job(Base):
    job_name = Column(String(2048))
    handler_name = Column(String(2024))
    start_processing_at = Column(DateTime)
    completed_at = Column(DateTime)
    payload = Column(String(16384))
    status = Column(Enum(JobStatus))
    result = Column(String(16384))
    logs = relationship(
        "JobLog",
        order_by=JobLog.updated_at,
        back_populates="job"
    )