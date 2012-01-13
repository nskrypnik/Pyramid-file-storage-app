from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.response import Response


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project':'dropline'}


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


@view_config(route_name='shere')
def shere_view(request):

    if request.method == 'POST':
        post_body = request.POST
        recipient_email = request.POST['email']
        link = request.POST['link']
        email_body = "Hello! You friend shere file with you:\n link to downloud: %s"  % link
        
        mailer = get_mailer(request)
        message = Message(subject="hello world",
                      sender="admin@mysite.com",
                      recipients=[recipient_email],
                      body=email_body )
                      
        mailer.send_immediately(message)
        return Response('Sacces send email' % request.matchdict)

    return Response('No POST data' % request.matchdict)
