from sqlalchemy import select

from app.core.db import AsyncSession
from app.models import CharityProject

from .base import CRUDBase


class CRUDProject(CRUDBase):

    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession
    ):
        obj_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        obj_id = obj_id.scalars().first()
        return obj_id

    async def get_check_full_amount(
        self, project_id: int, new_full_amount: int, session: AsyncSession
    ):
        obj_invested_amount = await session.execute(
            select(CharityProject.invested_amount).where(
                CharityProject.id == project_id
            )
        )
        obj_invested_amount = obj_invested_amount.scalars().first()
        return new_full_amount >= obj_invested_amount


project_crud = CRUDProject(CharityProject)
