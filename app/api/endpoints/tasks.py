from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.api.schemas.task import TaskCreate, TaskEdit, TaskFromDB
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
async def change_task(task: TaskEdit, session: AsyncSession = Depends(get_async_session)):
    updated_task = await session.get(Task, task.id)
    if not updated_task:
        raise HTTPException(404, detail={'message': 'Task not found'})
    
    updated_task.title = task.title
    updated_task.description = task.description

    await session.commit()

    return {'id': task.id, 'title': task.title, 'description': task.description}

@task_router.delete('/')
async def change_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    print(1)
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(404, detail={'message': 'task not found'})

    await session.delete(task)
    await session.commit()
    print(2)
    return {'id': task_id}
