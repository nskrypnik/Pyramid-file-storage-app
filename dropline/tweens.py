from pyramid.httpexceptions import HTTPFound
from pyramid.security import *

def auth_factory(handler, registry):
     def auth_tween(request):
        response = handler(request)       
        if authenticated_userid(request):
            return response
        
        exclude_paths = ["/login", "/logout", "/openid_send"]    

        if request.path in exclude_paths or request.path.find('/static') != -1:
            return response
        else:
            url = request.route_url('login') 
            return HTTPFound(location=url)

     return auth_tween

