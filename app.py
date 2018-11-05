from flask import Flask, render_template, request, session, redirect

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.secret_key = 'key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

engine = create_engine(
    'postgres://usetpxuboatswg:14291d4b50681090072617602611ea12822484a1e39cde28e9f046fc7ff50a85@ec2-54-235-86-226.'
    'compute-1.amazonaws.com:5432/d5mk3psi9hs4nb')
db = scoped_session(sessionmaker(bind=engine))


@app.route('/', methods=['GET', 'POST'])
def index():

    if session.get('username') is None:
        return redirect('/login')

    if request.method == 'GET':

        return render_template('index.html')

    else:

        query = request.form.get('query').lower()
        query_like = '%' + query + '%'

        books = db.execute('SELECT * FROM books WHERE (LOWER(isbn) LIKE :query) OR (LOWER(title) LIKE :query) '
                           'OR (LOWER(author) LIKE :query)',
                           {'query': query_like}).fetchall()

        if not books:
            return render_template('error.html', message='No Books were Found!')

        return render_template('result.html', query=query, books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():

    session.clear()

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user_id = db.execute('SELECT id FROM users WHERE (username=:username AND password=:password)',
                             {'username': username, 'password': password}).fetchall()

        if user_id is None:
            return render_template('error.html', message='Entered credentials not valid!')

        session["username"] = username

        return redirect('/')

    else:
        return render_template('login.html')


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    session.clear()

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        retype_password = request.form.get('retype_password')

        # check if passwords are the same

        if not password == retype_password:
            return render_template('error.html', message='Passwords do not match')

        # check if user is available

        avail = db.execute('SELECT username FROM users WHERE username=:username',
                           {'username': username}).fetchone()

        if avail:
            return render_template('error.html', message='Username Already Exists')

        # Write username and password to database

        db.execute('INSERT INTO users(username, password) VALUES(:username, :password)',
                   {'username': username, 'password': password})
        db.commit()

        session['username'] = username

        return redirect('/')

    else:
        return render_template('signup.html')