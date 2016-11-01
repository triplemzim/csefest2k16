from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import requires_csrf_token
from cseday2016.form_message import SubmitMessage

@requires_csrf_token
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



#@requires_csrf_token
def submit(request):

    error = {'has_error':False}
    # form = SubmitMessage(request.POST)
    # if form.is_valid():
    #     return render_to_response('index.html',{},context_instance = RequestContext(request))
    # else:
    return render_to_response('<p>I am the boss!</p>', {'error':error},context = RequestContext(request))