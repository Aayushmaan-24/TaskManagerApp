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
    
    return {
        "status" : "Task created successfully!",
        "data" : new_task
    }
    
    
def get_all_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    
    return {
        "status" : "Tasks fetched successfully!",
        "data" : tasks
    }
    
    
def get_task_by_id(task_id: int, db:Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!")
    return {
        "status" : "Task fetched successfully!",
        "data" : task
    }