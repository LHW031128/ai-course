import os

from flask import Flask, abort, redirect, render_template, request, url_for

import db

MAX_TITLE = 100

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo.db")


def database():
    return app.config["DATABASE"]


def show_list(error=None, status=200):
    return render_template("index.html", todos=db.list_todos(database()), error=error), status


@app.get("/")
def index():
    return show_list()


@app.post("/add")
def add():
    title = request.form.get("title", "")
    if not title:
        return show_list("제목을 입력하세요.", 400)
    if len(title) > MAX_TITLE:
        return show_list(f"제목은 {MAX_TITLE}자 이하로 입력하세요.", 400)
    db.add_todo(database(), title)
    return redirect(url_for("index"))


@app.post("/toggle/<int:todo_id>")
def toggle(todo_id):
    if not db.toggle_todo(database(), todo_id):
        abort(404)
    return redirect(url_for("index"))


@app.post("/delete/<int:todo_id>")
def delete(todo_id):
    if not db.delete_todo(database(), todo_id):
        abort(404)
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.init_db(database())
    app.run(debug=True)
