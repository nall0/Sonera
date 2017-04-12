from flask import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import *
from database import db_session

# -------- Create database and users table----------
from database import init_db
init_db()
# --------------------------------------------------
nbUsers=0
# ------- Function countNbUsers --------------------
def countNbUsers():
	global nbUsers
	nbUsers = 0
	for row in User.query.all():
		nbUsers += 1
	return nbUsers
# ------- Function addUser() -----------------------
def addUser(first_name, last_name, password):
	from database import db_session
	from users import User
	from users import User
	global nbUsers
	new_user = User(first_name, last_name, password)
	db_session.add(new_user)
	db_session.commit()
	nbUsers += 1
# --------------------------------------------------

# ------- Create Flask server ----------------------
app = Flask(__name__)
app.secret_key = 'stytjyntil468kyjnmti65468'  

# ------- Routes ----------------------------------
@app.route('/')
def index():
	addUser('Jesus', 'Christ', 'ninja')
	txt = "Salut"
	logged = 'logged' in session   
	if logged:
		txt = "Salut %d" % nbUsers                       
	return render_template('sigin.html', logged=logged, message=txt)

@app.route('/login', methods=['POST'])
def login():
	session['id'] = escape(request.form['id'])
	session['password'] = escape(request.form['password_sigin'])
	session['logged'] = True
	return redirect('/')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')
	
@app.route('/signup', methods=['POST'])
def signup():
	session['password'] = escape(request.form['password_sigup'])
	session['first_name'] = escape(request.form['first_name'])
	session['last_name'] = escape(request.form['last_name'])
	addUser(session['first_name'], session['last_name'], session['password'])
	session['id'] = nbUsers
	session['logged'] = True
	return redirect('/')

@app.route('/home', methods=['POST'])
def home():
    
    return render_template('home.html', first_name=, last_name=, , biography=)

if __name__ == '__main__':
	app.run(debug=True)

# ----------------- Method to close session at the end of request or application -----------
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

