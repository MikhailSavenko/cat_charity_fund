from pydantic import BaseModel, Field, validator
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


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[int] = Field(None, gt=0)

    @validator('full_amount')
    def update_validate_full_amoount(cls, value, values):
        if value <= values.get('invested_amount', 0):
            raise ValueError('full_amount не может быть меньше уже внесенной суммы')
        return value