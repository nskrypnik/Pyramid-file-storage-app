from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
#from .security import groupfinder
from dropline.models.meta import initialize_sql
from sqlalchemy import engine_from_config
from pyramid_mailer.mailer import Mailer
from pyramid.request import Request
from pyramid.decorator import reify
from pyramid.request import Request

from dropline.filestorage import initialize_file_storage


dropline_session_factory = UnencryptedCookieSessionFactoryConfig('helloworld')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    class DroplineRequest(Request):
        _server_port = settings.get('server.port') 
        _server_url = settings.get('server.url')
        _twitter_key = settings.get('consumer_secret')

        @property
        def server_url(self):
            if self._server_port:
                return "%s:%s" % (self._server_url, self._server_port)
            return self._server_url

        @property
        def twitter_key(self):
            if self._twitter_key:
                return self._twitter_key
            return self._twitter_key
                    
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    initialize_file_storage(settings.get('aws.access_key_id'),
                            settings.get('aws.secret_access_key'),
                            settings.get('s3.bucket'))
    
    authn_policy = AuthTktAuthenticationPolicy(secret='')
                       
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, session_factory = dropline_session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)

    config.add_tween('dropline.tweens.auth_factory')
    config.set_request_factory(DroplineRequest)
    
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('openid_send', '/openid_send')

    config.add_route('index', '/')
    config.add_route('uploader', '/uploader')

    config.add_route('shere', '/shere')
    mailer = Mailer()
    config.include('pyramid_mailer')
    config.registry['mailer'] = Mailer.from_settings(settings)

    config.scan()
    
    return config.make_wsgi_app()
    

