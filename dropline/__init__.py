from pyramid.config import Configurator
from pyramid_mailer.mailer import Mailer



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('index', '/index')
    config.add_route('uploader', '/uploader')
    config.add_route('shere', '/shere')
    mailer = Mailer()
    config.include('pyramid_mailer')
    config.registry['mailer'] = Mailer.from_settings(settings)

    config.scan()
    
    return config.make_wsgi_app()
