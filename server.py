from flask import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import *
from database import db_session


# website for SQLAlchemy+Flask (declarative base) : http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/

nbUsers=0
userList=None
resultFound=False

# ------- Function checkEmail --------------------
def checkEmail(email):
	from users import User
	for row in User.query.all():
		if row.email == email:
			print("Email already used !")
			return False
	return True

# --------- Function
def userSearch(dest, country=None):
	global userList
	from users import User
	if country == None:
		userList = User.query.filter(User.dest == dest)
		resultFound=True
	else:
		userList = User.query.filter(User.dest == dest and User.country == country)
		resultFound=True


# ------- Function countNbUsers --------------------
def countNbUsers():
	global nbUsers
	from users import User
	nbUsers = 0
	for row in User.query.all():
		nbUsers += 1
	return nbUsers
# ------- Function addUser() -----------------------
def addUser(email, first_name, last_name, password, biography, g , c, sch):
	from database import db_session
	from users import User
	global nbUsers
	new_user = User(email, first_name, last_name, password, biography, g, c, sch)
	db_session.add(new_user)
	db_session.commit()
	nbUsers += 1
# ---------------- Methode which test the password ------------------------
def pw_verification(email, password):
	from users import User
	current_user = User.query.filter(User.email == session['email']).first()
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
	return render_template('SignAdrien.html', logged=logged, nbUsers=nbUsers)

@app.route('/login', methods=['POST'])
def login():
	session['email'] = escape(request.form['email'])
	session['password'] = escape(request.form['password_sigin'])
	from users import User
	current_user = User.query.filter(User.email == session['email']).first()
	if current_user == None:
		return redirect('/')
	elif pw_verification(session['email'], session['password']):
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
	session['email'] = escape(request.form['email'])
	session['password'] = escape(request.form['password_sigup'])
	session['first_name'] = escape(request.form['first_name'])
	session['last_name'] = escape(request.form['last_name'])
	session['biography'] = escape(request.form['biography'])
	session['gender'] = escape(request.form['gender'])
	session['country'] = escape(request.form['country'])
	session['school'] = escape(request.form['school'])
	if checkEmail(session['email']):
		addUser(session['email'], session['first_name'], session['last_name'], session['password'], session['biography'], session['gender'], session['country'], session['school'])
		session['id'] = nbUsers
		session['logged'] = True
	return redirect('/')

@app.route('/profile')
def profile():
	from users import User
	current_user = User.query.filter(User.email == session['email']).first()
	bio = current_user.biography
	return render_template('profile0.html', first_name=session['first_name'], last_name=session['last_name'], biography=bio,
		country=session['country'], school=session['school'], gender=session['gender'], dest=session['dest'])

@app.route('/editProfile')
def editProfile():
	return render_template('editProfile.html', first_name=session['first_name'], last_name=session['last_name'], password=session['password'], country=session['country'], school=session['school'], biography=session['biography'], dest=session['dest'])

@app.route('/getNewInfos', methods=['POST', 'GET'])
def getNewInfos():
	from users import User
	current_user = User.query.filter(User.email == session['email']).first()
	session['password'] = escape(request.form['password_sigup'])
	current_user.password=session['password']
	session['first_name'] = escape(request.form['first_name'])
	current_user.first_name=session['first_name']
	session['last_name'] = escape(request.form['last_name'])
	current_user.last_name=session['last_name']
	session['biography'] = escape(request.form['biography'])
	current_user.biography=session['biography']
	session['country'] = escape(request.form['country'])
	current_user.country=session['country']
	session['dest'] = escape(request.form['dest'])
	current_user.dest=session['dest']
	session['school'] = escape(request.form['school'])
	current_user.school=session['school']
	return redirect('/profile')

@app.route('/getSearch', methods=['POST', 'GET'])
def getSearch():
	search_dest = escape(request.form['search_dest'])
	search_country = escape(request.form['search_country'])
	#on appelle userSearch soit avec juste la dest, soit avec dest puis country
	userSearch(search_dest, search_country)
	return redirect('/home')

@app.route('/home', methods=['POST', 'GET'])
def home():
	return render_template('home.html', first_name=session['first_name'], last_name=session['last_name'], email=session['email'], userList=userList, resultFound=resultFound)
# ------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	app.run(debug=True)

# ----------------- Method to close session at the end of request or application -----------
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
