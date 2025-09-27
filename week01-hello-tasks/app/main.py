from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Week 1 - Hello Tasks")

class Task(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=100)
    done: bool = False
    
TASKS: list[Task] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    if any(t.id == task.id for t in TASKS):
        raise HTTPException(status_code=400, detail="Task ID already exists")
    TASKS.append(task)  
    return task

@app.get("/tasks", response_model=list[Task])
def list_tasks(done: Optional[bool] = None):
    """
    Query param `done` is optional:
      - /tasks            → returns all
      - /tasks?done=true  → only completed
      - /tasks?done=false → only pending
    """
    if done is None:
        return TASKS
    return [t for t in TASKS if t.done == done]
    