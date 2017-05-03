from flask import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import *
from database import db_session


# website for SQLAlchemy+Flask (declarative base) : http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/

nbUsers=0
# ------- Function countNbUsers --------------------
def countNbUsers():
	global nbUsers
	from users import User
	nbUsers = 0
	for row in User.query.all():
		nbUsers += 1
	return nbUsers
# ------- Function addUser() -----------------------
def addUser(pseudo, first_name, last_name, password, biography, g , c, dest, sch):
	from database import db_session
	from users import User
	global nbUsers
	new_user = User(pseudo, first_name, last_name, password, biography, g, c, dest, sch)
	db_session.add(new_user)
	db_session.commit()
	nbUsers += 1
# ---------------- Methode which test the password ------------------------
def pw_verification(pseudo, password):
	from users import User
	current_user = User.query.filter(User.pseudo == session['pseudo']).first()
	real_password = current_user.password
	if real_password == password:
		return True
	else:
		return False
# --------------------------------------------------


# -------- Create database and users table----------
from database import init_db
init_db()
# --------------------------------------------------

# ------- Create Flask server ----------------------
app = Flask(__name__)
app.secret_key = 'stytjyntil468kyjnmti65468'


# ------- Routes ----------------------------------
@app.route('/')
def index():
	logged = 'logged' in session
	nbUsers = countNbUsers()
	if logged:
		return redirect('/home')
	return render_template('sigin.html', logged=logged, nbUsers=nbUsers)

@app.route('/login', methods=['POST'])
def login():
	session['pseudo'] = escape(request.form['pseudo'])
	session['password'] = escape(request.form['password_sigin'])
	from users import User
	current_user = User.query.filter(User.pseudo == session['pseudo']).first()
	if current_user == None:
		return redirect('/')
	elif pw_verification(session['pseudo'], session['password']):
		session['id'] = current_user.id
		session['first_name'] = current_user.first_name
		session['last_name'] = current_user.last_name
		session['biography'] = current_user.biography
		session['gender'] = current_user.gender
		session['country'] = current_user.country
		session['dest'] = current_user.dest
		session['school'] = current_user.school
		session['logged'] = True
	return redirect('/')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
	session['pseudo'] = escape(request.form['pseudo'])
	session['password'] = escape(request.form['password_sigup'])
	session['first_name'] = escape(request.form['first_name'])
	session['last_name'] = escape(request.form['last_name'])
	session['biography'] = escape(request.form['biography'])
	#session['gender'] = escape(request.form['gender'])
	#session['country'] = escape(request.form['country'])
	#session['dest'] = escape(request.form['dest'])
	#session['country'] = escape(request.form['country'])
	addUser(session['pseudo'], session['first_name'], session['last_name'], session['password'], session['biography'], session['gender'], session['country'], session['dest'], session['school'])
	session['id'] = nbUsers
	session['logged'] = True
	return redirect('/')

@app.route('/profile0')
def profile0():
	from users import User
	current_user = User.query.filter(User.id == session['id']).first()
	bio = current_user.biography
	return render_template('profile0.html', first_name=session['first_name'], last_name=['last_name'], biography=bio)

@app.route('/home', methods=['POST', 'GET'])
def home():
	return render_template('home.html', first_name=session['first_name'], last_name=session['last_name'], pseudo=session['pseudo'])
# ------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	app.run(debug=True)

# ----------------- Method to close session at the end of request or application -----------
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
