
from app.core.db import AsyncSession
from fastapi import HTTPException
from app.crud.charityproject import project_crud


async def check_name_duplicate(project_name: str, session: AsyncSession) -> None:
    """Проверяем уникальность поля name"""
    obj_id = await project_crud.get_project_id_by_name(project_name, session)
    if obj_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Название не уникальное!'
        )


async def chek_project_befor_edit(project_id: int, session: AsyncSession):
    """Проверяем существование объекта. Возвращаем его при наличии"""
    project = await project_crud.get(obj_id=project_id, session=session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Проекта не существует!'
        )
    return project