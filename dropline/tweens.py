from pyramid.httpexceptions import HTTPFound
from pyramid.security import *

def auth_factory(handler, registry):
     def auth_tween(request):
        response = handler(request)       
        if authenticated_userid(request):
            return response
            
        elif request.path == "/login":

            return response   

        else:
            url = request.route_url('login') 
            return HTTPFound(location=url)

     return auth_tween

