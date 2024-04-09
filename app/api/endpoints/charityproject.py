from fastapi import APIRouter, Depends
from app.api.validators import check_name_duplicate
from app.core.db import get_async_session, AsyncSession
from app.crud.charityproject import project_crud
from app.schemas.charityproject import ProjectDB, ProjectCreate
from app.core.user import current_superuser, current_user

router = APIRouter()

@router.get('/', response_model=list[ProjectDB])
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    projects = await project_crud.get_multi(session=session)
    return projects

@router.post('/', response_model=ProjectDB, dependencies=[Depends(current_superuser)])
async def create_new_project(project: ProjectCreate, session: AsyncSession = Depends(get_async_session)):
    await check_name_duplicate(project.name, session)
    project = await project_crud.create(obj_in=project, session=session)
    return project