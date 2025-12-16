from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.api.schemas.task import TaskCreate, TaskFromDB
from app.db.models import Task
from app.db.database import get_async_session


task_router = APIRouter(
    prefix='/task',
    tags=['Task']
)


@task_router.post('/', response_model=TaskFromDB)
async def create_tasks(task: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    new_task = Task(**task.model_dump())

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return new_task

@task_router.get('/', response_model=list[TaskFromDB])
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Task))
    return result.scalars().all()

@task_router.put('/')
async def change_task(task: TaskFromDB, session: AsyncSession = Depends(get_async_session)):
    updated_task = await session.get(Task, task.id)
    if not updated_task:
        return {'status': 'error'}
    
    updated_task.title = task.title
    updated_task.description = task.description
    updated_task.completed = task.completed

    await session.commit()

    return {'status': 'success'}

@task_router.delete('/')
async def change_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    await session.execute(delete(Task).where(Task.id == task_id))
    await session.commit()

    return {'status': 'success'}
