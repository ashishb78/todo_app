from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://NstmpRBITSfiZZfLLQoeSajdVaKceJNt:iswSXeCMnUXrsxFEEcNLnjbKrolWcBIe@db.thin.dev/16ff3dd6-099f-421a-9245-428e05b68151'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    # Show all todos
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list= todo_list)

@app.route("/add", methods= ["POST"])
def add():
    # Add new item
    title = request.form.get("title")
    new_todo = Todo(title= title, complete= False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    #app.run(debug= True)