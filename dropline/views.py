from pyramid.view import view_config
import hashlib
from pyramid.security import authenticated_userid
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
    )
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.renderers import render

from dropline.models.users import User
from dropline.models.meta import session, Session

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    logged_in = authenticated_userid(request)
    try:
        name = User.query.filter(User.email == logged_in).first().name
    except:
        name = User.query.filter(User.twitter == logged_in).first().name

    return {'project':'dropline', 'logged_in': logged_in, 'name': name} 
   
@view_config(route_name='login', renderer='templates/login.pt')
def login(request):
    #login_url = request.resource_url(request.context, 'login')
    #referrer = request.url
    #if referrer == login_url:
    #    referrer = '/' # never use the login form itself as came_from
    #came_from = request.params.get('came_from', referrer)
    message = ''
    
    if 'form.submitted' in request.params:
        login_name = request.params['login']
        login_type = request.params['login_type']
        login_id = request.params['login_id']

        if User.query.filter(User.email == login_id).first() or User.query.filter(User.twitter == login_id).first():
            consumer_secret = "tvKZebc83uxHllyOImgaAbF0k2nETwPaTWEbecSwlno"
            userID = request.cookies["twitter_anywhere_identity"].split(':')[0]
            digestfromtwitter = request.cookies["twitter_anywhere_identity"].split(':')[1]
            if hashlib.sha1(userID + consumer_secret).hexdigest() == digestfromtwitter:
                headers = remember(request, login_id)
                url = request.route_url('home') 
                return HTTPFound(location=url, headers = headers)    
            message = "Wrong information"
                      
        else:
            if login_type == "twitter":
                consumer_secret = "tvKZebc83uxHllyOImgaAbF0k2nETwPaTWEbecSwlno"
                userID = request.cookies["twitter_anywhere_identity"].split(':')[0]
                digestfromtwitter = request.cookies["twitter_anywhere_identity"].split(':')[1]
                if hashlib.sha1(userID + consumer_secret).hexdigest() == digestfromtwitter:
                    u = User(name = login_name, twitter = login_id)
                    session.add(u)
                    session.commit()
                    headers = remember(request, login_id)
                    url = request.route_url('home') 
                    return HTTPFound(location=url, headers = headers)
                message = "Wrong information"               
            else:
                u = User(name = login_name, email = login_id)
                session.add(u)
                session.commit()
                headers = remember(request, login_id)
                url = request.route_url('home') 
                return HTTPFound(location=url, headers = headers)                

    return dict(
        message = message,
        )
@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    result = render('templates/logout.pt', {}, request=request)
    response = Response(result)

    response.headerlist.extend(headers)
    return response


from pyramid.renderers import render_to_response


@view_config(route_name='index')
def index_view(request, template_name = 'templates/index.pt'):
    list_of_files = None

    return render_to_response(template_name, {'project':'dropline', 'list_of_files': list_of_files}, request=request)


@view_config(route_name='uploader')
def upload_view(request, template_name = 'templates/complete.pt'):

    if request.method == 'POST':
        post_body = request.POST
        file_name = request.POST['file'].filename
        return render_to_response(template_name, {  'post_body': post_body,
                                                    'file_name': file_name,
                                                    }, request=request)

    return render_to_response(template_name, {}, request=request)


