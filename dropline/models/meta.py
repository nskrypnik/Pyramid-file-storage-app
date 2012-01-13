from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

engine = create_engine('sqlite:///dev.db', convert_unicode=True, echo=True)
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))
session = Session()
Base.query = Session.query_property()


def init_db():
    from dropline.models.files import File
    from dropline.models.users import User
    Base.metadata.create_all(bind=engine)

