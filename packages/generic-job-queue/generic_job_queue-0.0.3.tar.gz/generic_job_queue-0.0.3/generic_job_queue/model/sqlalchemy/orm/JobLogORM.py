from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .ORMBase import Base


class JobLog(Base):
    message = Column(String(8192))
    job_id = Column(Integer, ForeignKey('job.id'))
    job = relationship("Job", back_populates="logs")
