
from app.core.db import AsyncSession
from fastapi import HTTPException
from app.crud.charityproject import project_crud


async def check_name_duplicate(project_name: str, session: AsyncSession) -> None:
    obj_id = await project_crud.get_project_id_by_name(project_name, session)
    if obj_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Название не уникальное!'
        )