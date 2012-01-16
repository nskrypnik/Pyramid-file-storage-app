from dropline.models.files import File
from dropline.models.users import User
from dropline.models.meta import Base
from sqlalchemy import engine_from_config
from pyramid.config import Configurator
from ConfigParser import ConfigParser

import sys

def init_db():

    config = ConfigParser()
    config.readfp(open("development.ini"))
    for key, value in config.items('app:main'):
        if key =='sqlalchemy.url':
            dic = {'sqlalchemy.url': value}
            engine = engine_from_config(dic, 'sqlalchemy.')
            print engine
    Base.metadata.create_all(bind=engine)
    
if __name__ == '__main__':
    init_db()
