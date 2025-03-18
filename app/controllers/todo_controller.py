from flask import Blueprint, render_template, request
from app.models.todo import Todo
from app.config.db import db

todo_blueprint = Blueprint("Todo", __name__, url_prefix="/todo")

@todo_blueprint.route("/", methods=["GET"])
def get_todos():
    todos = []
    if request.args:
        done = request.args.get("done")
        todos = Todo.query.filter(Todo.done == done).all()
    else:
        todos = Todo.query.all()
    return render_template("todos_index.html", todos = todos)

@todo_blueprint.route("/<int:id>", methods=["GET"])
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return render_template("todo_index.html", todo = todo)

@todo_blueprint.route("/create", methods=["GET"])
def create_todo():
    if request.args:
        name = request.args.get("name")
        description = request.args.get("description")

        new_todo = Todo(title=name, description=description)
        db.session.add(new_todo)
        db.session.commit()
        return "Se creó con éxito"
    return "No tiene argumentos la url"

@todo_blueprint.route("/update/<int:id>", methods=["GET"])
def update_todo(id):
    if request.args:
        todo = Todo.query.get_or_404(id)
        name = request.args.get("name")
        description = request.args.get("description")

        todo.title = name
        todo.description = description

        db.session.commit()
        return "Se modificó con éxito"
    return "No tiene argumentos la url"

@todo_blueprint.route("/delete/<int:id>", methods=["GET"])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return get_todos()





