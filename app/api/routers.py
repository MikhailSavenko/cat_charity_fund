from app.api.endpoints import project_router, user_router
from fastapi import APIRouter

main_router = APIRouter()


main_router.include_router(project_router, prefix='/charityproject', tags=['Charity Project'])
main_router.include_router(user_router)