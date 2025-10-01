from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI(title="Week 1 - Hello Tasks")

class Task(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=100)
    done: bool = False
    
class TaskUpdate(BaseModel):
    done: Optional[bool] = None


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
def list_tasks(
    done: Optional[bool] = None,
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    sort_by: Literal["id", "title"] = "id",
    order: Literal["asc", "desc"] = "asc",
):
    items = TASKS if done is None else [t for t in TASKS if t.done == done]

    # pick a key function safely
    key_fn = (lambda t: t.id) if sort_by == "id" else (lambda t: t.title.lower())

    # reverse if needed, then paginate
    items = sorted(items, key=key_fn, reverse=(order == "desc"))
    return items[offset : offset + limit]
    
@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, patch: TaskUpdate):
    """
    If body is empty or {"done": null} → toggle.
    If {"done": true|false} → set explicitly.
    """
    for t in TASKS:
        if t.id == task_id:
            if patch.done is None:
                t.done = not t.done
            else:
                t.done = patch.done
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """
    Remove a task by id.
    - 204 No Content on success (no body returned)
    - 404 if the task doesn't exist
    """
    global TASKS
    before = len(TASKS)
    TASKS = [t for t in TASKS if t.id != task_id]
    if len(TASKS) == before:
        raise HTTPException(status_code=404, detail="Task not found")
