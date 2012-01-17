import os.path
import uuid

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from dropline.models.meta import Base
from dropline.models.users import User
from dropline.filestorage import FileStorage

storage = FileStorage()

class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, Sequence('file_id_seq'), primary_key=True)
    uuid = Column(String(50)) #36
    title = Column(String(50))
    link = Column(String(50))
    mime_type = Column(String(50))
    user_id = Column(Integer, ForeignKey('users.id'))


    user = relationship("User", backref=backref('files', order_by=id))

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        if not 'uuid' in kwargs:
            self.uuid = str(uuid.uuid4())
   # def __init__(self, title, link, user_id):
   #     self.title = title
   #     self.link = link
   #     self.user_id = user_id


    def __repr__(self):
        return "<File('%s,%s')>" % (self.title, self.user_id)
        
    @hybrid_method
    def save(self, data):
        if not self.title and self.uuid:
            return False
        if self.mime_type:
            content_type = self.mime_type
        else:
            content_type = None
        return storage.send_file(self.uuid, data, content_type)
        
    @hybrid_method
    def get_url(self, expires_in=None):
        if not self.uuid:
            return None
        return storage.generate_url(self.uuid, expires_in)

