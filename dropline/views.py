from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
    )
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.renderers import render

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    logged_in = authenticated_userid(request)

    return {'project':'dropline', 'logged_in': logged_in} 
   
@view_config(route_name='login', renderer='templates/login.pt')
def login(request):

    login_url = request.resource_url(request.context, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        #password = request.params['password']
        #if USERS.get(login) == password:
        if login == "Bogdan":
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )
@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    result = render('templates/logout.pt', {}, request=request)
    response = Response(result)

    response.headerlist.extend(headers)
    return response

    #return dict(headers = headers)#HTTPFound(location = request.resource_url(request.context),
                     

