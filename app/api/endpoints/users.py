import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.schemas.user import UserLogin, UserReg
from app.core.security import create_access_token
from app.db.models import User

from app.db.database import get_async_session



user_router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@user_router.post('/login')
async def login(user_info: UserLogin, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).where(
        User.username == user_info.username,
        User.password == user_info.password,
    ))
    if not user.scalars().all():
        logging.error('Ошибка при регистрации: Пользователь не найден')
        raise HTTPException(404, detail={'message': 'user not found'})

    logging.info(f'Вход в аккаунт: {user_info.username}')
    token = create_access_token({'sub': user_info.username})
    return {'access_token': token, 'token_type': 'bearer'}

@user_router.post('/')
async def register(user: UserReg, session: AsyncSession = Depends(get_async_session)):
    search_user = await session.execute(select(User).where(User.username == user.username))
    if search_user.scalars().all():
        logging.error('Ошибка при регистрации: Пользователь уже существует')
        raise HTTPException(401, detail={'message': 'User already exists'})
    
    new_user = User(**user.model_dump())

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    logging.info(f'Зарегистрирован новый пользователь: {new_user}')
    return new_user
