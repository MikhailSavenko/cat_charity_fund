from .base import CRUDBase
from app.models import CharityProject
from app.core.db import AsyncSession
from sqlalchemy import select


class CRUDProject(CRUDBase):

    async def get_project_id_by_name(self, project_name: str, session: AsyncSession):
        obj_id = await session.execute(select(CharityProject.id).where(CharityProject.name==project_name))
        obj_id = obj_id.scalars().first()
        return obj_id
    
    async def get_check_full_amount(self, project_id: int, new_full_amount: int, session: AsyncSession):
        obj_invested_amount = await session.execute(select(CharityProject.invested_amount).where(CharityProject.id==project_id))
        obj_invested_amount = obj_invested_amount.scalars().first()
        if new_full_amount < obj_invested_amount:
            return False
        return True


project_crud = CRUDProject(CharityProject)