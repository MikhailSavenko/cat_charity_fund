from fastapi import APIRouter, Depends
from app.core.db import get_async_session, AsyncSession
from app.models import User
from app.schemas.donation import DonationCreate, DonationCurrentUserDB, DonationSuperUserDB
from app.core.user import current_superuser, current_user
from app.crud.donation import danation_crud
from app.services.investing import investing_donat

router = APIRouter()


@router.get('/', response_model=list[DonationSuperUserDB], dependencies=[Depends(current_superuser)])
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    donations = await danation_crud.get_multi(session=session)
    return donations

@router.post('/', response_model=DonationCurrentUserDB, dependencies=[Depends(current_user)])
async def create_donation(donation: DonationCreate, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    donation = await danation_crud.create(obj_in=donation, session=session, user=user)
    donation = await investing_donat(obj_donat=donation, session=session)
    return donation

@router.get('/my', response_model=list[DonationCurrentUserDB], dependencies=[Depends(current_user)])
async def get_my_donations(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    donations = await danation_crud.get_by_user(user=user, session=session)
    return donations