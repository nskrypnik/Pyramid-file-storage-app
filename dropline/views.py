from pyramid.view import view_config
from pyramid.renderers import render_to_response

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



