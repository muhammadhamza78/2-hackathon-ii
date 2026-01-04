"""
Task CRUD API Endpoints
FastAPI router for task create, read, update, delete operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timezone
from app.db.session import get_session
from app.auth.dependencies import get_current_user_id
from app.models.task import Task
from app.schemas.task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TaskListResponse
)

router = APIRouter(tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    task = Task(
        title=request.title,
        description=request.description,
        status=request.status,
        user_id=user_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return TaskResponse.from_orm(task)


@router.get("", response_model=TaskListResponse, status_code=status.HTTP_200_OK)
async def list_tasks(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskListResponse:
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    ).all()
    return TaskListResponse(tasks=[TaskResponse.from_orm(t) for t in tasks])


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse.from_orm(task)


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if request.title is not None:
        task.title = request.title
    if request.description is not None:
        task.description = request.description
    if request.status is not None:
        task.status = request.status

    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return TaskResponse.from_orm(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> None:
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    session.delete(task)
    session.commit()
    return None
