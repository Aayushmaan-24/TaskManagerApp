from fastapi import APIRouter, Depends, status
from src.utils.db import get_db
from src.tasks import controller
from src.tasks.dtos import TaskSchema, TaskResponseSchema

task_routes = APIRouter(prefix="/tasks")



@task_routes.post("/create", response_model=TaskResponseSchema,  status_code=status.HTTP_201_CREATED)
def create_task(body: TaskSchema, db = Depends(get_db)):
    return controller.create_task(body, db)

@task_routes.get("/all_tasks", status_code=status.HTTP_200_OK)
def get_all_tasks(db = Depends(get_db)):
    return controller.get_all_tasks(db)

@task_routes.get("/task/{task_id}", status_code=status.HTTP_200_OK)
def get_task_by_id(task_id: int, db = Depends(get_db)):
    return controller.get_task_by_id(task_id, db)

@task_routes.put("/update/{task_id}", status_code=status.HTTP_201_CREATED)
def update_task(task_id: int, body: TaskSchema, db = Depends(get_db)):
    return controller.update_task(task_id, body, db)

@task_routes.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db = Depends(get_db)):
    return controller.delete_task(task_id, db)