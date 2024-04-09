from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: int = Field(gt=0)
    

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
    pass
    # нужна валидация поля full_amount только суперюзер и не ниже уже внесенной суммы