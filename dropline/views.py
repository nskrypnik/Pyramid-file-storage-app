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
from pyramid.renderers import render_to_response
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.response import Response
#from gdocs.lib_gdoc import Gdoc
import lib_gdoc
from openid.store.filestore import FileOpenIDStore
from openid.consumer.consumer import Consumer, DiscoveryFailure, SUCCESS, FAILURE, SETUP_NEEDED, SETUP_NEEDED
from openid.extensions import sreg, ax
import tempfile
import cgi
from dropline.models.files import File


SERVER_OPENID = 'https://www.google.com/accounts/o8/id'
ROOT = 'http://localhost:6543/'
RETURN_TO = ROOT + 'login' 
STORAGE = FileOpenIDStore(tempfile.gettempdir())
   
@view_config(route_name='login', renderer='templates/login.pt')
def login(request):
    message = ''
    if 'openid.ns' in request.GET:
        consumer = Consumer(request.session, STORAGE)
        info = consumer.complete(request.POST or request.GET, "%s/login" % request.server_url)
        if info.status == FAILURE:
            message = "Verification failed: %s" % info.message
        elif info.status == SUCCESS:
            ax_response = ax.FetchResponse.fromSuccessResponse(info)
            sreg_response = sreg.SRegResponse.fromSuccessResponse(info)
            if ax_response:
                login_name= "%s %s" % (ax_response.get('http://axschema.org/namePerson/first')[0], ax_response.get('http://axschema.org/namePerson/last')[0])
                login_id=ax_response.get('http://axschema.org/contact/email')[0]
            else:
                login_name=sreg_response.get('nickname')[0]
                login_id=sreg_response.get('email')[0]

            if not User.query.filter(User.email == login_id).first():
                u = User(name = login_name, email = login_id)
                print u
                session.add(u)
                session.commit()
            
            headers = remember(request, login_id)
            url = request.route_url('index')
            return HTTPFound(location=url, headers = headers) 
                

        elif info.status == CANCEL:
            message = 'Verification cancelled'
        elif info.status == SETUP_NEEDED:
            if info.setup_url: message = '<a href=%s>Setup needed</a>' % ( '"%s"' % cgi.escape(info.setup_url, 1) ,)
            else: message = 'Setup needed'
        else: message = 'Verification failed.'
        return dict(
            message = message,
            )

    elif 'form.submitted' in request.params:
        login_name = request.params['login']
        login_type = request.params['login_type']
        login_id = request.params['login_id']
        consumer_secret = request.twitter_key
        
        if User.query.filter(User.email == login_id).first() or User.query.filter(User.twitter == login_id).first():
            userID = request.cookies["twitter_anywhere_identity"].split(':')[0]
            digestfromtwitter = request.cookies["twitter_anywhere_identity"].split(':')[1]
            if hashlib.sha1(userID + consumer_secret).hexdigest() == digestfromtwitter:
                headers = remember(request, login_id)
                url = request.route_url('index') 
                return HTTPFound(location=url, headers = headers)    
            message = "Wrong information"
              
        else:
            if login_type == "twitter":
                userID = request.cookies["twitter_anywhere_identity"].split(':')[0]
                digestfromtwitter = request.cookies["twitter_anywhere_identity"].split(':')[1]
                if hashlib.sha1(userID + consumer_secret).hexdigest() == digestfromtwitter:
                    u = User(name = login_name, twitter = login_id)
                    session.add(u)
                    session.commit()
                    headers = remember(request, login_id)
                    url = request.route_url('index') 
                    return HTTPFound(location=url, headers = headers)
                message = "Wrong information"               
        
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



@view_config(route_name='index', renderer='templates/index.pt')
def index_view(request):
    logged_in = authenticated_userid(request)
    
    user = User.query.filter(User.email == logged_in).first()
    if user is None:
        user = User.query.filter(User.twitter == logged_in).first()
    if user is None:
        list_of_files = []
    else:
        list_of_files = File.query.filter(File.user_id == user.id).all()

    return { 'list_of_files': list_of_files, 'project': 'dropline'}



@view_config(route_name='uploader')
def upload_view(request, template_name = 'templates/complete.pt'):
    if request.method == 'POST':
        logged_in = authenticated_userid(request)
        user = User.query.filter(User.email == logged_in).first()
        if user is None:
            user = User.query.filter(User.twitter == logged_in).first()
        file_to_upload = request.POST['file']
        am_file = File(title=file_to_upload.filename,
                       mime_type=file_to_upload.type,
                       user_id=user.id)
        
        session.add(am_file)
        session.commit()
        
        return render_to_response(template_name, {  'file_name': am_file.title,
                                                    'file_link': am_file.link,
                                                    }, request=request)

    return render_to_response(template_name, {}, request=request)


@view_config(route_name='shere')
def shere_view(request):

    if request.method == 'POST':
        post_body = request.POST
        recipient_email = request.POST['email']
        link = request.POST['link']
        email_body = "Hello! You friend shere file with you:\n link to download: %s"  % link
        
        mailer = get_mailer(request)
        message = Message(subject="hello world",
                      sender="admin@mysite.com",
                      recipients=[recipient_email],
                      body=email_body )
                      
        mailer.send_immediately(message)
        return Response('Sacces send email' % request.matchdict)

    return Response('No POST data' % request.matchdict)



@view_config(route_name='openid_send')
def doVerify(request):
    try:
        consumer = Consumer(request.session, STORAGE)
        openid_request = consumer.begin(SERVER_OPENID)
    except DiscoveryFailure, exc:
        message = 'Error in discovery: %s' % ( cgi.escape(str(exc[0])) )
        return dict(
            message = message,
        )
    else:
        if openid_request is None:
            message = 'No OpenID services found for <code>%s</code>' % ( cgi.escape(openid_url),)
            return dict(
                message = message,
            )
        else:
            requestReg(openid_request)
            redirect_url = openid_request.redirectURL(request.server_url, "%s/login" % request.server_url)
            return HTTPFound(location=redirect_url)

def requestReg(request):
    if request.endpoint.supportsType(ax.AXMessage.ns_uri):
        fetch_request = ax.FetchRequest()
        for (attr, alias) in [
            ('http://axschema.org/contact/email', 'email'),
            ('http://axschema.org/namePerson', 'fullname'),
            ('http://axschema.org/namePerson/first', 'firstname'),
            ('http://axschema.org/namePerson/last', 'lastname'),
            ('http://axschema.org/pref/language', 'language'),
            ('http://axschema.org/contact/country/home', 'country')]:
            fetch_request.add(ax.AttrInfo(attr, alias=alias, required=True))
        request.addExtension(fetch_request)
    else:
        request.addExtension(sreg.SRegRequest(optional=['email', 'fullname', 'nickname'
                                                        # for vkontakte
            ,'gender','country']))
