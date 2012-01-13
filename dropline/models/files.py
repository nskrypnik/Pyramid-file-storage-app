from sqlalchemy import *
from sqlalchemy.orm import *
from dropline.models.meta import Base
from dropline.models.users import User

class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, Sequence('file_id_seq'), primary_key=True)
    uuid = Column(String(50))
    title = Column(String(50))
    link = Column(String(50))
    mime_type = Column(String(50))
    user_id = Column(Integer, ForeignKey('users.id'))


    user = relationship("User", backref=backref('files', order_by=id))

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
   # def __init__(self, title, link, user_id):
   #     self.title = title
   #     self.link = link
   #     self.user_id = user_id


    def __repr__(self):
        return "<File('%s,%s')>" % (self.title, self.user_id)
