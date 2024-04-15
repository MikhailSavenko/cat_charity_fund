from app.core.db import AsyncSession
from fastapi import HTTPException
from app.crud.charity_project import project_crud


async def check_change_full_amount(
    project_id, new_full_amount: int, session: AsyncSession
):
    """Новая сумма сбора не ниже уже собранной"""
    full_amount = await project_crud.get_check_full_amount(
        project_id, new_full_amount, session
    )
    if not full_amount:
        raise HTTPException(
            status_code=400,
            detail='full_amount не может быть меньше уже внесенной суммы',
        )


async def check_name_duplicate(
    project_name: str, session: AsyncSession
) -> None:
    """Проверяем уникальность поля name"""
    obj_id = await project_crud.get_project_id_by_name(project_name, session)
    if obj_id is not None:
        raise HTTPException(status_code=400, detail='Название не уникальное!')


async def chek_project_befor_edit(project_id: int, session: AsyncSession):
    """Проверяем существование объекта. Возвращаем его при наличии"""
    project = await project_crud.get(obj_id=project_id, session=session)
    if not project:
        raise HTTPException(status_code=404, detail='Проекта не существует!')
    if project.fully_invested:
        raise HTTPException(status_code=400, detail='Проект уже завершен')
    return project


async def chek_project_invested_amount(project: int, session: AsyncSession):
    """Проверяем наличие пожертвований у проекта перед удалением"""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='Удалить невозможно. Проект уже получил пожертвование.',
        )
    return project
