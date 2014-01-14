from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PickleType, LargeBinary
from jutsu.lib.db import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class FileBackup(Base):
	__tablename__ = 'backups'
	id = Column(Integer, primary_key=True)
	task_id = Column(Integer, ForeignKey('tasks.id'))
	path = Column(String)
	content = Column(LargeBinary)
	timestamp = Column(DateTime)
	
	def __repr__(self):
		return '<FileBackup %r from: %r>' % (self.path, self.timestamp)


class Task(Base):
	__tablename__ = 'tasks'
	id = Column(Integer, primary_key=True)
	kind = Column(String)
	started = Column(DateTime)
	finished = Column(DateTime)
	config = Column(PickleType)
	flow_id = Column(Integer, ForeignKey('plans.id'))
	backups = relationship('FileBackup', backref='task', lazy='dynamic')
	
	__mapper_args__ = {
		'polymorphic_identity':'task',
		'polymorphic_on':kind
    }

	def __init__(self, kind=None, **config):
		self.kind = kind
		self.config = config

	def __repr__(self):
		return '<Task %r, started: %r, finished: %r>' % (self.kind, self.started, self.finished)
	
	def do(self):
		self.started = datetime.utcnow()
	
	def undo(self):
		pass

class Plan(Base):
	__tablename__ = 'plans'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	created = Column(DateTime)
	executed = Column(DateTime)
	current_task = Column(Integer)
	tasks = relationship('Task', backref='plan', lazy='dynamic')

	def __init__(self, name=None):
		self.name = name
		self.created = datetime.utcnow()
		self.current_task = 0

	def execute(self):
		self.executed = datetime.utcnow()
		while self.current_task < len(self.tasks):
			task = self.tasks[self.current_task]
			try:
				task.do()
				task.executed = datetime.utcnow()
			except Exception:
				break
			++self.current_task