from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from dt.telegram.models import Base


class Category(Base):
    __tablename__ = "categories"  # noqa

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    jobs = relationship(
        "Job", back_populates="category", cascade="all, delete-orphan"
    )


class Job(Base):
    __tablename__ = "jobs"  # noqa

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    link = Column(String, nullable=False)
    formatted = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="jobs")
