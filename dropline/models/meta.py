from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import MetaData


__all__ = ['Base', 'Session']

metadata = MetaData()

Session = scoped_session(sessionmaker())
Base = declarative_base(metadata=metadata)
Base.query = Session.query_property()

def initialize_sql(engine):
    Session.configure(bind=engine,expire_on_commit=False)
    Base.metadata.bind = engine
 

