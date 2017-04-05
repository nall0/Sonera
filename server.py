from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *

# ------- Function addUser() --------
def addUser(first_name, last_name, password):
	connection.execute(users.insert(), [
		{'first_name': first_name, 'last_name': last_name, 'password': password}])

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
addUser('Jesus', 'Christ', 'ninja') 

# ------- Create Flask server ---------
app = Flask(__name__)
app.secret_key = 'stytjyntil468kyjnmti65468'  

# ------- Routes ---------
@app.route('/')
def index():
	logged = 'logged' in session   
	if logged:
		print(session['id'])                             
	return render_template('sigin.html', logged=logged)

@app.route('/login', methods=['POST'])
def login():
	session['id'] = escape(request.form['id'])
	session['password'] = escape(request.form['password'])
	session['logged'] = True
	return render_template('sigin.html', logged=logged, identifiant=session['id'])
	#return redirect('/')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')
	
@app.route('/signup')
def signup():
	session['id'] = escape(request.form['id'])
	session['password'] = escape(request.form['password'])
	session['first_name'] = escape(request.form['first_name'])
	session['last_name'] = escape(request.form['last_name'])
	addUser(session['first_name'], session['last_name'], session['password'])

if __name__ == '__main__':
	app.run(debug=True)
	

connection.close() 
