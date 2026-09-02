from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Complete Python practice", "done": False},
    {"id": 2, "title": "Prepare for interview", "done": True},
]
next_id = 3

HTML = """
<!doctype html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Student Task Manager</title>
    <style>
        body { font-family: Arial, sans-serif; background:#f4f6f8; margin:0; }
        .container { max-width:650px; margin:40px auto; padding:20px; }
        .card { background:white; padding:25px; border-radius:14px; box-shadow:0 3px 14px rgba(0,0,0,.08); }
        h1 { margin-top:0; }
        form.add { display:flex; gap:8px; margin-bottom:20px; }
        input { flex:1; padding:12px; border:1px solid #ccc; border-radius:8px; }
        button { padding:12px 16px; border:0; border-radius:8px; cursor:pointer; }
        .add button { background:#222; color:white; }
        ul { list-style:none; padding:0; }
        li { display:flex; align-items:center; justify-content:space-between; padding:12px 0; border-bottom:1px solid #eee; }
        .done { text-decoration:line-through; color:#888; }
        .actions { display:flex; gap:6px; }
        .actions button { background:#eee; }
        .delete { background:#f1dede !important; }
        .empty { color:#777; text-align:center; padding:20px; }
        @media(max-width:600px){ .container{margin:10px auto;} form.add{flex-direction:column;} }
    </style>
</head>
<body>
<div class="container">
  <div class="card">
    <h1>🎓 Student Task Manager</h1>
    <p>Organize your study and career tasks in one place.</p>

    <form class="add" method="post" action="/add">
      <input name="title" placeholder="Enter a new task..." required>
      <button type="submit">Add Task</button>
    </form>

    {% if tasks %}
    <ul>
      {% for task in tasks %}
      <li>
        <span class="{{ 'done' if task.done else '' }}">{{ task.title }}</span>
        <div class="actions">
          <form method="post" action="/toggle/{{ task.id }}">
            <button type="submit">{{ 'Undo' if task.done else 'Done' }}</button>
          </form>
          <form method="post" action="/delete/{{ task.id }}">
            <button class="delete" type="submit">Delete</button>
          </form>
        </div>
      </li>
      {% endfor %}
    </ul>
    {% else %}
      <div class="empty">No tasks yet. Add your first task!</div>
    {% endif %}
  </div>
</div>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML, tasks=tasks)

@app.post("/add")
def add():
    global next_id
    title = request.form.get("title", "").strip()
    if title:
        tasks.append({"id": next_id, "title": title, "done": False})
        next_id += 1
    return redirect(url_for("home"))

@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("home"))

@app.post("/delete/<int:task_id>")
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("home"))

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
