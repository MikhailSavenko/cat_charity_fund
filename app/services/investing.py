from app.models import Donation, CharityProject
from sqlalchemy import select, func, desc
from app.core.db import AsyncSession


def change_value_attr(obj_in, investing_sum):
    obj_in.invested_amount += investing_sum
    obj_in.fully_invested = True
    obj_in.close_date = func.now()
    return obj_in


async def investing_donat(obj_donat: Donation, session: AsyncSession):
    full_amount_donat = obj_donat.full_amount
    all_open_projects = await session.execute(select(CharityProject).where(CharityProject.fully_invested == False).order_by(desc(CharityProject.create_date)))
    all_open_projects = all_open_projects.scalars().all()
    if not all_open_projects:
        return obj_donat

    inveing_amount_now = 0
    index_project = 0
    while inveing_amount_now != full_amount_donat and index_project < len(all_open_projects):
        project = all_open_projects[index_project]
        required_donation = project.full_amount - project.invested_amount
        if required_donation == full_amount_donat - inveing_amount_now:
            # для проекта
            change_value_attr(project, required_donation)
            # для доната
            change_value_attr(obj_donat, required_donation)
            inveing_amount_now += required_donation
        elif required_donation < full_amount_donat - inveing_amount_now:
            # донат
            obj_donat.invested_amount += required_donation
            if obj_donat.invested_amount == full_amount_donat:
                # донат проинвестирован
                obj_donat.fully_invested = True
                obj_donat.close_date = func.now()
            else:
                # проект
                change_value_attr(project, required_donation)
                inveing_amount_now += required_donation
        elif required_donation > full_amount_donat - inveing_amount_now:
            donation_balance = full_amount_donat - inveing_amount_now
            # для объекта доната
            change_value_attr(obj_donat, donation_balance)
            # проект
            project.invested_amount += donation_balance
            inveing_amount_now += donation_balance
        index_project += 1
        # добавим объекты в сессию
        session.add(project)
        session.add(obj_donat)
    await session.commit()
    await session.refresh(obj_donat)
    return obj_donat


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
        if donat_free == full_amount_project - amount_now:
            # для объекта проекта
            change_value_attr(obj_project, donat_free)
            # для объекта доната
            change_value_attr(donat, donat_free)
            # для выхода из цикла
            amount_now += donat_free
        elif donat_free < full_amount_project - amount_now:
            # для объекта проекта ТРАБЛЫ ДОБАВЛЯЕМ сразу даже не зная сколько надо добавить
            obj_project.invested_amount += donat_free
            # проверяем о необходимости закрытия сборов проекта
            if obj_project.invested_amount == full_amount_project:
                obj_project.fully_invested = True
                obj_project.close_date = func.now()
                # для объекта доната
                change_value_attr(donat, donat_free)
                # для увеличения счетчика выхода из цикла
                amount_now += donat_free
            else:
                # для объекта доната
                change_value_attr(donat, donat_free)
                # для увеличения счетчика выхода из цикла
                amount_now += donat_free
        elif donat_free > full_amount_project - amount_now:
            # найдем сумму требуемой инвестиции в проект на данный момент
            investing_sum = full_amount_project - amount_now
            # для объекта проекта
            change_value_attr(obj_project, investing_sum)
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
