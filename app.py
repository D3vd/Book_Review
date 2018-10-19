from flask import Flask, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine('')
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    return 'Hello World'
