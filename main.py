from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List,Optional
from uuid import UUID, uuid4

app = FastAPI()

class Task(BaseModel):
    id:Optional[UUID]=None
    title:str
    description:Optional[str]=None
    completed:bool=False


tasks=[]


@app.post("/tasks/",response_model=Task)
async def create_task(task:Task):
    task.id=uuid4()
    tasks.append(task)
    return task

@app.get("/tasks/",response_model=List[Task])
async def read_tasks():
    return tasks

@app.get("/task/{task_id}",response_model=Task)
async def read_task(task_id:UUID):
    for task in tasks:
        if task.id==task_id:
            return task
        
    raise HTTPException(status_code=404,detail="Task not found!")

@app.put("/task/{task_id}",response_model=Task)
async def update_task(task_id:UUID,task_update:Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task=task.copy(update=task_update.dict(exclude_unset=True))
            tasks[idx]=updated_task
            return updated_task
    
    raise HTTPException(status_code=404,detail="Task not found!")

@app.delete("/task/{task_id}",response_model=Task)
async def delete_task(task_id:UUID):
    for idx,task in enumerate(tasks):
        if task.id==task_id:
            return tasks.pop(idx)
        
    raise HTTPException(status_code=404,detail="Task not found!")


