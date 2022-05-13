from flask import Flask, render_template, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import sqlalchemy
from sqlalchemy import text, Table, Column, Integer, String, select, func, cast


app = Flask(__name__)

# Data DB engine queries
engine = sqlalchemy.create_engine("sqlite+pysqlite:///data.db", future=True)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		if not request.form.get("login"):
			print("HTTP400: Type Something.")
			return redirect("/")

		return render_template("update.html")
	else:
		#TODO: Show top 3 entries.
		dates = []
		entries = []
		with engine.connect() as conn:
			results = conn.execute(text("SELECT date, entry FROM entries ORDER BY date DESC"))
			for row in results:
				dates.append(row["date"])
				entries.append(row["entry"])

		#TODO: Calendar stuff

		return render_template("index.html", dates=dates, entries=entries)

@app.route("/update", methods=["GET", "POST"])
def update():
	if request.method == "POST":
		entry = request.form.get("entry")
		# TODO: Ability to submit a new entry
		print(entry)

		return redirect("/")
	else:
		return render_template("update.html")

@app.route("/aboutme")
def aboutme():
	# TODO: Fix the image/text flex problem
	return render_template("aboutme.html")

@app.route("/projects")
def projects():
	# TODO: Add some actual projects maybe...
	return render_template("projects.html")

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")
