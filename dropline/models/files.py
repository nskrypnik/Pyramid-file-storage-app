import os.path
import uuid

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from dropline.models.meta import Base, Session
from dropline.models.users import User
from dropline.filestorage import FileStorage
import urllib

storage = FileStorage()

GD_VIEWER = 'http://docs.google.com/viewer?'

SUPPORTED_FILETYPES = {
  'CSV': 'text/csv',
  'TSV': 'text/tab-separated-values',
  'TAB': 'text/tab-separated-values',
  'DOC': 'application/msword',
  'DOCX': ('application/vnd.openxmlformats-officedocument.'
           'wordprocessingml.document'),
  'ODS': 'application/x-vnd.oasis.opendocument.spreadsheet',
  'ODT': 'application/vnd.oasis.opendocument.text',
  'RTF': 'application/rtf',
  'SXW': 'application/vnd.sun.xml.writer',
  'TXT': 'text/plain',
  'XLS': 'application/vnd.ms-excel',
  'XLSX': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'PDF': 'application/pdf',
  'PNG': 'image/png',
  'PPT': 'application/vnd.ms-powerpoint',
  'PPS': 'application/vnd.ms-powerpoint',
  'HTM': 'text/html',
  'HTML': 'text/html',
  'ZIP': 'application/zip',
  'SWF': 'application/x-shockwave-flash'
  }

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
        self.session = Session()

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
            
        self.session.add(self)
        self.session.commit()
        return storage.send_file(self.uuid, data, content_type)
        
    @hybrid_method
    def get_url(self, expires_in=None):
        if not self.uuid:
            return None
        return storage.generate_url(self.uuid, expires_in)
        
    
    @hybrid_method
    def get_gd_url(self, expires_in=None):
        if self.mime_type in SUPPORTED_FILETYPES.values():
            file_url = self.get_url()
            gd_url = "".join([GD_VIEWER, urllib.urlencode({'url': file_url})])
            return gd_url
        return self.get_url()
    
    
