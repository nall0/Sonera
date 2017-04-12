from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, autoincrement=True)
	first_name = Column(String)
	last_name = Column(String)
	password = Column(String)

	def __init__(self, first_name=None, last_name=None, password=None):
		self.first_name = first_name
		self.last_name = last_name
		self.password = password

	def __repr__(self):
		return '<User %s, %s, %s>' % (self.id, self.first_name, self.last_name)