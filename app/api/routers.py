from app.api.endpoints import project_router, user_router, donation_router
from fastapi import APIRouter

main_router = APIRouter()


main_router.include_router(project_router, prefix='/charity_project', tags=['Charity Project'])
main_router.include_router(donation_router, prefix='/donation', tags=['Donation'])
main_router.include_router(user_router)