from .base import CRUDBase
from app.models import CharityProject
from app.core.db import AsyncSession
from sqlalchemy import select

class CRUDProject(CRUDBase):

    async def get_project_id_by_name(self, project_name: str, session: AsyncSession):
        obj_id = await session.execute(select(CharityProject.id).where(CharityProject.name==project_name))
        obj_id = obj_id.scalars().first()
        return obj_id

project_crud = CRUDProject(CharityProject)