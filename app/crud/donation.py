from app.models import User, Donation
from .base import CRUDBase
from app.models import Donation
from app.core.db import AsyncSession
from sqlalchemy import select


class CRUDDonation(CRUDBase):

    async def get_by_user(self, user: User, session: AsyncSession):
        donations_user = await session.execute(select(Donation).where(Donation.user_id == user.id))
        donations_user = donations_user.scalars().all()
        return donations_user


danation_crud = CRUDDonation(Donation)