from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import path

DB_PATH = '/var/lib/jutsu/app.db'

engine = create_engine('sqlite:///' + DB_PATH, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Authomatically create database if not exists:
if not path.exists(DB_PATH):
    import jutsu.lib.models  # @UnusedImport
    Base.metadata.create_all(bind=engine)
