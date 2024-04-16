from sqlalchemy import select

from app.core.db import AsyncSession
from app.models import Donation, User

from .base import CRUDBase


class CRUDDonation(CRUDBase):

    async def get_by_user(self, user: User, session: AsyncSession):
        donations_user = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        donations_user = donations_user.scalars().all()
        return donations_user


danation_crud = CRUDDonation(Donation)
