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
		txt = 'Bonjour %s !' % session['id']
	return render_template('index_sessions.html', message=txt, logged=logged)

@app.route('/login', methods=['POST'])
def login():
	session['id'] = escape(request.form['id'])
	session['password'] = escape(request.form['password'])
	session['logged'] = True
	return redirect('/')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)
	

connection.close() 
