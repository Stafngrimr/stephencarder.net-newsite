from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from tempfile import mkdtemp


import sqlalchemy
from sqlalchemy import text, Table, Column, Integer, String, select, func, cast

from helpers import login_required

app = Flask(__name__)

# Ensure templates are auto-reloaded + secret key
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'17%^uefr2fhn-0-1$.,j'

# Data DB engine queries
engine = sqlalchemy.create_engine("sqlite+pysqlite:///data.db")

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		if not request.form.get("login"):
			print("HTTP400: Type Something.")
			return redirect("/")

		with engine.connect() as conn:
			user = conn.execute(text("SELECT * FROM users"))
			for row in user:
				print(row["hash"])

		
		password2 = "3563A56801227AFEAA618181B62E15F08AD5FC21"

		if not check_password_hash(password2, request.form.get("login")):
			print("HTTP403: Wrong Password.")
			print(password2)
			print(request.form.get("login"))
			return redirect("/")

		return redirect("/update")

	else:
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
@login_required
def update():
	if request.method == "POST":
		entry = request.form.get("entry")
		# TODO: Ability to submit a new entry
		print(entry)

		return redirect("/")
	else:
		return render_template("update.html")

@app.route("/aboutme", methods=["GET", "POST"])
def aboutme():
	if request.method == "POST":
		name = request.form.get("user")
		pa = request.form.get("password")
		hash = generate_password_hash(pa, method="sha256", salt_length=8)
		with engine.connect() as conn:
			conn.execute(text("INSERT INTO users (name, hash) VALUES (?, ?)", name, hash))
		return redirect("/")

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
