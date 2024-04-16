from fastapi import APIRouter, Depends

from app.api.validators import (check_change_full_amount, check_name_duplicate,
                                chek_project_invested_amount,
                                get_project_or_404)
from app.core.db import AsyncSession, get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.schemas.charity_project import ProjectCreate, ProjectDB, ProjectUpdate
from app.services.investing import investing_money

router = APIRouter()


@router.get('/', response_model=list[ProjectDB])
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    return await project_crud.get_multi(session=session)


@router.post(
    '/', response_model=ProjectDB, dependencies=[Depends(current_superuser)]
)
async def create_new_project(
    project: ProjectCreate, session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(project.name, session)
    project = await project_crud.create(obj_in=project, session=session)
    project = await investing_money(obj_project=project, session=session)
    return project


@router.delete(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    project = await get_project_or_404(project_id, session)
    await chek_project_invested_amount(project, session)
    project_del = await project_crud.remove(db_obj=project, session=session)
    return project_del


@router.patch(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    obj_in: ProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project_obj_db = await get_project_or_404(project_id, session)
    await check_name_duplicate(obj_in.name, session)
    full_amount_update = obj_in.full_amount
    if full_amount_update is not None:
        await check_change_full_amount(project_id, obj_in.full_amount, session)
    project_update = await project_crud.update(
        db_obj=project_obj_db, obj_in=obj_in, session=session
    )
    return project_update
