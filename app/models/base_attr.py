from sqlalchemy import Column, Integer, DateTime, Boolean, func
from app.core.db import Base


class BaseAttr(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=func.now())
    close_date = Column(DateTime, default=None)