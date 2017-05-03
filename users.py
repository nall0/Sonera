from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, autoincrement=True)
	pseudo = Column(String, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	password = Column(String)
	biography = Column(String)
	country = Column(String)
	dest = Column(String)
	school = Column(String)
	gender = Column(String)

	def __init__(self, pseudo=None, first_name=None, last_name=None, password=None, bio=None, g=None, c=None, s=None):
		self.first_name = first_name
		self.last_name = last_name
		self.password = password
		self.pseudo = pseudo
		self.biography = bio
		self.gender = g
		self.country = c
		self.dest = None
		self.school = s

	def __repr__(self):
		return '<User %s, %s, %s, biography : %s>' % (self.pseudo, self.first_name, self.last_name, self.biography)
