from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException, status


def create_task(body: TaskSchema, db:Session):
    data = body.model_dump()
    
    new_task = TaskModel(**data)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task
    
    
def get_all_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    
    return tasks
    
    
def get_task_by_id(task_id: int, db:Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!")
    return task
    
    
def update_task(task_id: int, body: TaskSchema, db:Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        return HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Task not found!")
    
    body = body.model_dump()
    for key, value in body.items():
        setattr(task, key, value)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task
    

def delete_task(task_id: int, db:Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!")
    
    db.delete(task)
    db.commit()
    
    return None