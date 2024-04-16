from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: int = Field(gt=0)


class DonationCreate(DonationBase):
    pass


class DonationCurrentUserDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationSuperUserDB(DonationCurrentUserDB):
    user_id: int
    close_date: datetime = None
    fully_invested: bool
    invested_amount: int

    class Config:
        orm_mode = True
