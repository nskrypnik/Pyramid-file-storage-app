from sqlalchemy import *
from dropline.models.meta import Base
from sqlalchemy.orm import *

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    twitter = Column(String(50))
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)



    def __repr__(self):
        return "<User('%s')>" % self.name
    

