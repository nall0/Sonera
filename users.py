from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, autoincrement=True)
	email = Column(String, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	password = Column(String)
	biography = Column(String)
	country = Column(String)
	dest = Column(String)
	school = Column(String)
	gender = Column(String)

	def __init__(self, email=None, first_name=None, last_name=None, password=None, biography=None, gender=None, country=None, s=None):
		self.email = email
		self.first_name = first_name
		self.last_name = last_name
		self.password = password
		self.biography = biography
		self.gender = gender
		self.country = country
		self.dest = ""
		self.school = s

	def __repr__(self):
		return '<User %s, %s, %s, biography : %s>' % (self.email, self.first_name, self.last_name, self.biography)
