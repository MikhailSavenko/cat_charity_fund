from app.models import Donation, CharityProject
from sqlalchemy import select, func
from app.core.db import AsyncSession


async def investing_money(obj_project: CharityProject, session: AsyncSession):
    full_amount_project = obj_project.full_amount
    all_donation_free = await session.execute(select(Donation).where(Donation.fully_invested == False))
    all_donation_free = all_donation_free.scalars().all()
    if not all_donation_free:
        return obj_project
    amount_now = 0
    index_donations = 0
    while amount_now != full_amount_project and index_donations < len(all_donation_free):
        donat = all_donation_free[index_donations]
        donat_free = donat.full_amount - donat.invested_amount
        if donat_free == full_amount_project:
            # для объекта проекта 
            obj_project.invested_amount += donat_free
            obj_project.fully_invested = True
            obj_project.close_date = func.now()
            # для объекта доната
            donat.invested_amount += donat_free
            donat.fully_invested = True
            donat.close_date = func.now()
            # для выхода из цикла
            amount_now += donat_free
        elif donat_free < full_amount_project:
            # для объекта проекта 
            obj_project.invested_amount += donat_free
            # проверяем о необходимости закрытия сборов проекта
            if obj_project.invested_amount == full_amount_project:
                obj_project.fully_invested = True
                obj_project.close_date = func.now()
                # для объекта доната
                donat.invested_amount += donat_free
                donat.fully_invested = True
                donat.close_date = func.now()
                # для увеличения счетчика выхода из цикла
                amount_now += donat_free
            else:
                # для объекта доната
                donat.invested_amount += donat_free
                donat.fully_invested = True
                donat.close_date = func.now()
                # для увеличения счетчика выхода из цикла
                amount_now += donat_free
        elif donat_free > full_amount_project:
            # найдем сумму требуемой инвестиции в проект на данный момент
            investing_sum = full_amount_project - amount_now
            # для объекта проекта
            obj_project.invested_amount += investing_sum
            obj_project.fully_invested = True
            obj_project.close_date = func.now()
            # для объекта доната
            donat.invested_amount += investing_sum
            amount_now += investing_sum
        index_donations += 1
        # добавим объекты в сессию
        session.add(donat)
        session.add(obj_project)
    await session.commit()
    await session.refresh(obj_project)
    return obj_project
