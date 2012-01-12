from pyramid.httpexceptions import HTTPFound
from pyramid.security import *

def auth_factory(handler, registry):
     def auth_tween(request):
        #import pdb; pdb.set_trace()
        response = handler(request)       
        if authenticated_userid(request):
            return response
            
        elif request.path == "/login":

            return response   
              
        elif request.path == "/logout":

            return response    
        else:
            url = request.route_url('login') 
            return HTTPFound(location=url)

     return auth_tween

     return handler

if __name__ == '__main__':
    print "Hello"
    class Dummy(object):
        pass
        
    req = Dummy() 
    req.session = {}
    auth = auth_factory('handler', 'registry')
    res = auth(req)
    print res.location
