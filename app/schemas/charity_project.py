from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(min_length=1)
    full_amount: int = Field(gt=0)

    class Config:
        extra = Extra.forbid


class ProjectCreate(ProjectBase):
    pass


class ProjectDB(ProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class ProjectUpdate(ProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)
