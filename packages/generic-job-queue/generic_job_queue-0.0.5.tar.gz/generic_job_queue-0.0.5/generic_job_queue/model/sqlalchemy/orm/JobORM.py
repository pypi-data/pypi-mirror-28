import uuid

from sqlalchemy import Column, String, Enum, DateTime, SmallInteger
from sqlalchemy.orm import relationship

from generic_job_queue.enum.job_status import JobStatus
from .ORMBase import Base
from .JobLogORM import JobLog
from .data_type import JSON_TYPE


class Job(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_name = Column(String(2048))
    handler_name = Column(String(2024), index=True)
    channel = Column(SmallInteger, default=0, index=True) # For support multi worker
    start_processing_at = Column(DateTime)
    completed_at = Column(DateTime)
    payload = Column(JSON_TYPE)
    job_meta = Column(JSON_TYPE)
    status = Column(Enum(JobStatus), index=True)
    result = Column(String(65535))
    logs = relationship(
        "JobLog",
        order_by=JobLog.updated_at,
        back_populates="job"
    )
