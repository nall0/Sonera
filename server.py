#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import *
from database import db_session

# website for SQLAlchemy+Flask (declarative base) : http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/

nbUsers=0
resultFound=False
userList = []
search_dest=""
search_country=""
# ------- Function checkEmail --------------------
def checkEmail(email):
	from users import User
	for row in User.query.all():
		if row.email == email:
			print("Email already used !")
			return False
	return True

# --------- Function userSearch
def userSearch(city, country):
	res=[]
	global resultFound
	from users import User
	if country == "":
		userList = User.query.filter(User.dest == city.upper())
	else:
		userList = User.query.filter(User.dest == city.upper()).filter(User.country == country.upper())
	print(userList)
	resultFound=True

	for u in userList:
		print(" ------------------ RES --------------")
		print(u.first_name)
		print(" --------------------------------")
		res.append(u.first_name)

	return userList


# ------- Function countNbUsers --------------------
def countNbUsers():
	global nbUsers
	from users import User
	nbUsers = 0
	for row in User.query.all():
		nbUsers += 1
	return nbUsers
# ------- Function addUser() -----------------------
def addUser(email, first_name, last_name, password, biography, g , c, sch, d):
	from database import db_session
	from users import User
	global nbUsers
	new_user = User(email, first_name, last_name, password, biography, g, c, sch, d)
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
	return render_template('SignUpIn.html', logged=logged, nbUsers=nbUsers)

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
	global userList
	userList = []
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
	session['country'] = escape(request.form['country']).upper()
	session['school'] = escape(request.form['school'])
	session['dest'] = escape(request.form['dest']).upper()
	if checkEmail(session['email']):
		addUser(session['email'], session['first_name'], session['last_name'], session['password'], session['biography'], session['gender'], session['country'], session['school'], session['dest'])
		session['id'] = nbUsers
		session['logged'] = True
	return redirect('/')

@app.route('/profile')
def profile():
	# clear list of results
	global userList
	global resultFound
	userList=[]
	resultFound=False
	search_dest=""
	# display template
	return render_template('profile0.html', email=session['email'], first_name=session['first_name'], last_name=session['last_name'], biography=session['biography'],
		country=session['country'], school=session['school'], gender=session['gender'], dest=session['dest'])


@app.route('/user:<email>')
def user(email):
	# clear list of results
	global userList
	global resultFound
	userList=[]
	search_dest=""
	resultFound=False
	# get infos in the database
	from users import User
	user_found = User.query.filter(User.email == email).first()
	return render_template('profileOfOthers.html', email=user_found.email, first_name=user_found.first_name, last_name=user_found.last_name,
		gender=user_found.gender, dest=user_found.dest, country=user_found.country, school=user_found.school, biography=user_found.biography)

@app.route('/editProfile', methods=['POST', 'GET'])
def editProfile():
	# clear list of results
	global userList
	global resultFound
	userList=[]
	search_dest=""
	resultFound=False

	return render_template('editProfile.html', first_name=session['first_name'], last_name=session['last_name'], password=session['password'],
		country=session['country'], school=session['school'], biography=session['biography'], dest=session['dest'])

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
	session['country'] = escape(request.form['country']).upper()
	current_user.country=session['country']
	session['dest'] = escape(request.form['dest']).upper()
	current_user.dest=session['dest']
	session['school'] = escape(request.form['school'])
	current_user.school=session['school']
	return redirect('/profile')

@app.route('/getSearch', methods=['POST', 'GET'])
def getSearch():
	global userList
	global search_dest
	global search_country
	userList = []
	search_dest = escape(request.form['search_dest'])
	search_country = escape(request.form['search_country'])
	print("============== search_country :", search_country)
	#on appelle userSearch soit avec juste la dest, soit avec dest puis country
	userList = userSearch(search_dest, search_country)

	return redirect('/home')

@app.route('/home', methods=['POST', 'GET'])
def home():
	global userList
	global search_dest
	global search_country
	global resultFound
	if resultFound:
		txt = "Students in " + search_dest
		if search_country != "":
			txt += " ("+search_country+")"
		txt += " :"
	else:
		txt=""
	return render_template('home.html', first_name=session['first_name'], last_name=session['last_name'],
	 	email=session['email'], resultBoxTitle=txt, resultFound=resultFound, result_list=userList)

@app.route('/rapport')
def rapport():
	return render_template('rapport.html')
# ------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	app.run(debug=True)

# ----------------- Method to close session at the end of request or application -----------
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
