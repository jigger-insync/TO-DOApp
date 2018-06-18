import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Item(db.Model):
    task = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Task: {}>".format(self.task)

@app.route("/", methods=["GET", "POST"])
def home():
	if request.form:
		try:
			item = Item(task=request.form.get("task"))
			db.session.add(item)
			db.session.commit()
		except IntegrityError:
			db.session.rollback()
			items = Item.query.all()
			error=True
			return render_template("home.html", items=items, error=error)

	items = Item.query.all()
	return render_template("home.html", items=items)
  
@app.route("/update", methods=["POST"])
def update():
	newtask = request.form.get("newtask")
	oldtask = request.form.get("oldtask")
	try:
		item = Item.query.filter_by(task=oldtask).first()
		item.task = newtask
		db.session.commit()
	except IntegrityError:
		error=True
		return redirect(url_for(".home", error=error))

	return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
	task = request.form.get("task")
	item = Item.query.filter_by(task=task).first()
	db.session.delete(item)
	db.session.commit()
	return redirect("/")