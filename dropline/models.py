from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    twitter = Column(String(50))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<User('%s')>" % self.name
    
class File(Base):
    __tablename__ = 'files'
    
    uuid = Column(String(50), primary_key=True)
    title = Column(String(50))
    link = Column(String(50))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref=backref('files', order_by=id))


    def __init__(self, title, link, user_id):
        self.title = title
        self.link = link
        self.user_id = user_id


    def __repr__(self):
        return "<File('%s,%s')>" % (self.title, self.user_id)
