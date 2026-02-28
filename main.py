from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI(title="Simple Todo API", version="1.0.0")
handler = Mangum(app)
# --- In-memory store ---
todos = {}
counter = 1


# --- Models ---
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False
    created_at: str


# --- Endpoints ---


@app.get("/")
def root():
    """Health check / welcome endpoint."""
    return {
        "message": "Welcome to the Todo API!",
        "status": "healthy",
        "time": datetime.now().isoformat(),
    }


@app.get("/todos", response_model=list[Todo])
def get_todos():
    """Return all todos."""
    return list(todos.values())


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoCreate):
    """Create a new todo item."""
    global counter
    todo = Todo(
        id=counter,
        title=payload.title,
        description=payload.description,
        done=False,
        created_at=datetime.now().isoformat(),
    )
    todos[counter] = todo
    counter += 1
    return todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, done: bool):
    """Mark a todo as done or not done."""
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id].done = done
    return todos[todo_id]


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a todo by ID."""
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return {"message": f"Todo {todo_id} deleted successfully"}
