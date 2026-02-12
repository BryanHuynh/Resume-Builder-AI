from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from db.base import Base


class CateredResume(Base):
    __tablename__ = "catered_resumes"
    __table_args__ = (
        UniqueConstraint("user_id", "job_name", name="uq_catered_resumes_user_job"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_name = Column(String(255), nullable=False)
    resume_data = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="catered_resumes")
