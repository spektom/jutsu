from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from jutsu.lib.db import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Task(Base):
	__tablename__ = 'tasks'
	id = Column(Integer, primary_key=True)
	kind = Column(String(120))
	started = Column(DateTime)
	finished = Column(DateTime)
	flow_id = Column(Integer, ForeignKey('flows.id'))

	def __init__(self, kind=None):
		self.kind = kind

	def __repr__(self):
		return '<Task %r, started: %r, finished: %r>' % (self.kind, self.started, self.finished)
	
	def do(self):
		self.started = datetime.utcnow()
	
	def undo(self):
		pass

class Flow(Base):
	__tablename__ = 'flows'
	id = Column(Integer, primary_key=True)
	name = Column(String(120))
	created = Column(DateTime)
	executed = Column(DateTime)
	tasks = relationship('Task', backref='flow', lazy='dynamic')

	def __init__(self, name=None):
		self.name = name
		self.created = datetime.utcnow()

	def execute(self):
		self.executed = datetime.utcnow()
