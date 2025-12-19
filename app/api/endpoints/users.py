from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.schemas.user import UserLogin, UserReg
from app.core.security import create_access_token
from app.db.models import User

from app.db.database import get_async_session



user_router = APIRouter(
    prefix='/user',
    tags=['User']
)


@user_router.post('/login')
async def login(user_info: UserLogin, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).where(
        User.username == user_info.username,
        User.password == user_info.password,
    ))
    if not user.scalars().all():
        raise HTTPException(404, detail={'message': 'user not found'})

    token = create_access_token({'sub': user_info.username})
    return {'access_token': token, 'token_type': 'bearer'}

@user_router.post('/')
async def register(user: UserReg, session: AsyncSession = Depends(get_async_session)):
    search_user = await session.execute(select(User).where(User.username == user.username))
    if search_user.scalars().all():
        raise HTTPException(400, detail={'message': 'User already exists'})
    
    new_user = User(**user.model_dump())

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user