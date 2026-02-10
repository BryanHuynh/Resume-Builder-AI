from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from db.base import Base


class Additional(Base):
    __tablename__ = "additionals"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(255))
    items = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="additionals")
