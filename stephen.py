from flask import Flask, render_template
import sqlalchemy
from sqlalchemy import create_engine, text


app = Flask(__name__)

# Data DB engine queries
engine = create_engine("sqlite+pysqlite:///data.db")

@app.route('/')
def index():

    return render_template("index.html")
