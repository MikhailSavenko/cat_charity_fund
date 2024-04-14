from fastapi import APIRouter, Depends
from app.api.validators import check_name_duplicate, chek_project_befor_edit
from app.core.db import get_async_session, AsyncSession
from app.crud.charityproject import project_crud
from app.schemas.charityproject import ProjectDB, ProjectCreate, ProjectUpdate
from app.core.user import current_superuser
from app.services.investing import investing_money

router = APIRouter()

@router.get('/', response_model=list[ProjectDB])
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    projects = await project_crud.get_multi(session=session)
    return projects

@router.post('/', response_model=ProjectDB, dependencies=[Depends(current_superuser)])
async def create_new_project(project: ProjectCreate, session: AsyncSession = Depends(get_async_session)):
    await check_name_duplicate(project.name, session)
    ### ТЕСТИМ СОЗДАНИЕ ПРОЕКТА 
    project = await project_crud.create(obj_in=project, session=session)
    project = await investing_money(obj_project=project, session=session)
    return project

@router.delete('/{project_id}', response_model=ProjectDB, dependencies=[Depends(current_superuser)])
async def delete_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    project = await chek_project_befor_edit(project_id, session)
    project_del = await project_crud.remove(db_obj=project, session=session)
    return project_del


@router.patch('/{project_id}', response_model=ProjectDB, dependencies=[Depends(current_superuser)])
async def update_project(project_id: int, obj_in: ProjectUpdate, session: AsyncSession = Depends(get_async_session)):
    project_obj_db = await chek_project_befor_edit(project_id, session)
    project_update = await project_crud.update(db_obj=project_obj_db, obj_in=obj_in, session=session)
    return project_update