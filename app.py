from flask import Flask, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine('postgres://usetpxuboatswg:14291d4b50681090072617602611ea12822484a1e39cde28e9f046fc7ff50a85@ec2-54-235-86-226.compute-1.amazonaws.com:5432/d5mk3psi9hs4nb')
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    return 'Hello World'
