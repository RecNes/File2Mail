from pyramid import config
from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/index.pt')
def index(request):
    return {'project': 'File2Mail'}

@view_config(route_name='docs', renderer='templates/docs.pt')
def docs(request):

    return {'project': 'Documents', 'documentation': 1}