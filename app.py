from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    todos = Todo.query.order_by(Todo.id).all()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    if text:
        db.session.add(Todo(text=text))
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5050)
