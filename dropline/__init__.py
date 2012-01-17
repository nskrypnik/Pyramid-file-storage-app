from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
#from .security import groupfinder
from dropline.models.meta import initialize_sql
from sqlalchemy import engine_from_config
from pyramid_mailer.mailer import Mailer

dropline_session_factory = UnencryptedCookieSessionFactoryConfig('helloworld')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    
    authn_policy = AuthTktAuthenticationPolicy(secret='')
                       
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, session_factory = dropline_session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)

    config.add_tween('dropline.tweens.auth_factory')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('index', '/index')
    config.add_route('uploader', '/uploader')

    config.add_route('shere', '/shere')
    mailer = Mailer()
    config.include('pyramid_mailer')
    config.registry['mailer'] = Mailer.from_settings(settings)

    config.scan()
    
    return config.make_wsgi_app()
