from pydantic import BaseModel, Field, validator, Extra
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(gt=0)

    class Config:
        extra = Extra.forbid


class ProjectCreate(ProjectBase):
    pass


class ProjectDB(ProjectBase):
    id: int
    # description: str # поменял
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

    # @validator('full_amount')
    # def update_validate_full_amount(cls, value: int, values):
    #     print(value)
    #     a = values.get("invested_amount")
    #     print(f'invested_amount = {a}')
    #     if value <= values.get('invested_amount', 0):
    #         print(values.get('invested_amount', 0))
    #         raise ValueError('full_amount не может быть меньше уже внесенной суммы')
    #     return value
