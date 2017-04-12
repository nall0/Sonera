from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *


# ------- Function addUser() --------
def addUser(first_name, last_name, password):
	connection.execute(users.insert(), [
		{'first_name': first_name, 'last_name': last_name, 'password': password}])
	global nbUsers
	nbUsers += 1
# ------- Function countNbUsers -----
def countNbUsers():
	nbUsers = 0
	for row in connection.execute(select([func.count(users.c.id)])):
		nbUsers += 1
	return nbUsers
# -----------------------------------

# -------- Create SQL tables ----------
engine = create_engine('sqlite:///sonera.db', echo=True)   
metadata = MetaData()                                     
users = Table('users', metadata,                          
            Column('id', Integer, autoincrement=True, primary_key=True),
            Column('first_name', String),
            Column('last_name', String),
            Column('password', String))
metadata.create_all(engine)                               
connection = engine.connect()
nbUsers = countNbUsers()
addUser('Jesus', 'Christ', 'ninja')

# ------- Create Flask server ---------
app = Flask(__name__)
app.secret_key = 'stytjyntil468kyjnmti65468'  

# ------- Routes ---------
@app.route('/')
def index():
	txt = "Salut"
	logged = 'logged' in session   
	if logged:
		txt = "Salut %s" % session['id']                             
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

if __name__ == '__main__':
	app.run(debug=True)
	

connection.close() 
