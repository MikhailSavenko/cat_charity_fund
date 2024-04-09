from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: int
    

class DonationCreate(DonationBase):
    pass


class DonationCurrentUserDB(DonationBase):
    id: int
    create_date: datetime


class DonationSuperUserDB(DonationCurrentUserDB):
    user_id: int
    close_date: datetime = None
    fully_invested: bool
    invested_amount: int
