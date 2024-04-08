from app.core.db import Base
from sqlalchemy import Column, Integer, DateTime, Boolean, func


class BaseAttr(Base):
    __tablename__ = None
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime, default=func.now())
    close_date = Column(DateTime, default=None)

    @property
    def close_date(self):
        if self.fully_invested:
            return func.now()
        return None