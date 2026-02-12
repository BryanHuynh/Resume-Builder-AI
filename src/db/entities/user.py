from sqlalchemy import Column, String, ARRAY, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50))
    city_province = Column(String(255))
    links = Column(ARRAY(Text))
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    sections = relationship("Section", back_populates="user", cascade="all, delete-orphan")
    additionals = relationship("Additional", back_populates="user", cascade="all, delete-orphan")
    catered_resumes = relationship("CateredResume", back_populates="user", cascade="all, delete-orphan")
