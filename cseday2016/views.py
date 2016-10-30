from django.template import RequestContext
from django.shortcuts import render_to_response



def index(request):
    """
    loads the initial web page showing the client the basic view of the website
    if the user is logged in then redirects the user to Newsfeed
    :param request: the HTMLRequest
    :return: either the index.html template if the user is not logged in
            or newsfeed if the user is logged in
    """
    context = RequestContext(request)
    error = {'has_error':False}
    return render_to_response('index.html', {'error':error}, context)