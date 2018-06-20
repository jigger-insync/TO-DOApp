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
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80), unique=True, nullable=False)
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return "<Task: {}>".format(self.task)

@app.route("/", methods=["GET", "POST"])
def home():
	error = request.args.get('error', False) # check for error, if no error then set to False
	if request.form:
		# check if update or add
		task = request.form.get("task", None)

		if task: # if task is not None, then it is add
			try:
				item = Item(task=request.form.get("task"))
				db.session.add(item)
				db.session.commit()
			except IntegrityError:
				db.session.rollback()
				error = True
		else:
			newtask = request.form.get("newtask")
			oldtask = request.form.get("oldtask")

			try:
				item = Item.query.filter_by(task=oldtask).first()
				item.task = newtask
				db.session.commit()
			except IntegrityError:
				db.session.rollback()
				error = True

	items = Item.query.all()
	return render_template("home.html", items=items, error=error)
	
@app.route("/delete", methods=["POST"])
def delete():
	task = request.form.get("task")
	item = Item.query.filter_by(task=task).first()
	db.session.delete(item)
	db.session.commit()
	return redirect("/")