from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.schemas.user import UserCreate, UserFromDB
from app.core.security import create_access_token
from app.db.models import User

from app.db.database import get_async_session



user_router = APIRouter(
    prefix='/user',
    tags=['User']
)


@user_router.post('/login')
async def login(user_info: UserCreate, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).where(User.email == user_info.email,\
                                                                    User.password == user_info.password))
    if not user:
        return {'status': 'error'}

    token = create_access_token({'sub': user_info.email})
    return {'access token': token, 'token_type': 'bearer'}

@user_router.post('/')
async def register(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(**user.model_dump())

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user