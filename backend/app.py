from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from db import SessionLocal
from models import Task, init_db
from ai import suggest_schedule
from datetime import datetime

load_dotenv()
app = Flask(__name__)
CORS(app)
init_db()

def to_dict(task: Task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "due": task.due.isoformat() if task.due else None,
        "duration_min": task.duration_min,
        "is_done": task.is_done,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }

# --- CRUD ---
@app.get("/api/tasks")
def list_tasks():
    db = SessionLocal()
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    db.close()
    return jsonify([to_dict(t) for t in tasks])

@app.post("/api/tasks")
def create_task():
    data = request.json or {}
    db = SessionLocal()
    t = Task(
        title=data.get("title", "Untitled"),
        description=data.get("description"),
        duration_min=data.get("duration_min"),
        is_done=data.get("is_done", False),
        due=datetime.fromisoformat(data["due"]) if data.get("due") else None,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    out = to_dict(t)
    db.close()
    return jsonify(out), 201

@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.json or {}
    db = SessionLocal()
    t = db.get(Task, task_id)
    if not t:
        db.close()
        return jsonify({"error": "not_found"}), 404
    for k in ["title", "description", "duration_min", "is_done"]:
        if k in data:
            setattr(t, k, data[k])
    if "due" in data:
        t.due = datetime.fromisoformat(data["due"]) if data["due"] else None
    db.commit()
    db.refresh(t)
    out = to_dict(t)
    db.close()
    return jsonify(out)

@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    db = SessionLocal()
    t = db.get(Task, task_id)
    if not t:
        db.close()
        return jsonify({"error": "not_found"}), 404
    db.delete(t)
    db.commit()
    db.close()
    return ("", 204)

@app.post("/api/ai/suggest")
def ai_suggest():
    db = SessionLocal()
    tasks = [to_dict(t) for t in db.query(Task).all()]
    db.close()
    plan = suggest_schedule(tasks)
    # return JSON (plan is already JSON text or dict depending on ai.py)
    return jsonify(plan)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)