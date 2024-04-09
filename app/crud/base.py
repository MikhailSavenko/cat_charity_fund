from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.models import User
from typing import Optional


class CRUDBase:

    def __init__(self, model):
        self.model = model
    
    async def get_multi(self, session: AsyncSession):
        """Возвращает список всех объектов"""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in, session: AsyncSession, user: Optional[User] = None):
        """Создает новый объект"""
        obj_in_data = obj_in.dict()
        print(obj_in_data)
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj 
