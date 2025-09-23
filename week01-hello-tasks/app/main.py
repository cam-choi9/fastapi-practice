from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

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